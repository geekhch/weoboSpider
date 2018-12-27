import time, json
from ..utils import __get_logger, DB, GET
from .url_tools import urlTools
from .parse_tools import parse_profile, parse_user, parse_weibo
import threading
import traceback

logger = __get_logger("spider")


class Spider:
    "根据功能爬去数据保存到数据库"
    urlTool = urlTools()
    weibo_lock = threading.Lock()  # 数据库写入锁
    user_col = DB.get_collection("user")

    def __init__(self, uid, blogs=False, fans_follow=False):
        """
        一键获取用户基本信息、所有微博、关注用户uid列表、粉丝用户uid列表，保存到db
        """
        self.uid = uid
        self.urlTool = urlTools()
        self.weibo_lock = threading.Lock()  # 数据库写入锁
        self.user_col = DB.get_collection("user")
        self.__end_page = False  # 线程控制使用成员变量
        self.frequency = 0.2  # 线程并发请求需要按照页码顺序（时间太短将导致服务器拒绝回应）
        logger.info("初始化%d" % uid)

        if not self.user_col.find_one({'_id': uid}):
            url = self.urlTool.profile_user(uid)
            data = parse_profile(GET(url))
            if data:
                self.user_col.replace_one({'_id': uid}, data, upsert=True)  # 新增字段而不是完全替换
            else:
                logger.info("profile无法解析：%s" % data)
                time.sleep(2)
                return

        if blogs:
            self.weibo_blogs()
        if fans_follow:
            self.fans_and_follow()

    def __weibo_spider_helper(self, url):
        """请求某一页的所有博客文章数据，并加入到数据库"""
        data = GET(url)
        try:
            data = json.loads(data)  # 一页10个微博文章
        except:
            # print(data)
            # traceback.print_exc()
            if not data:
                print("请求过于频繁...")
                return
            print(url, '获取失败，重新获取...')
            self.__weibo_spider_helper(url)
            return

        if data['ok'] == 0:
            if 'msg' in data and data['msg'] == '这里还没有内容':
                self.__end_page = True
                return
            if 'msg' in data and data['msg'] == '请求过于频繁,歇歇吧':
                logger.info("线程请求频繁，开始休眠1s")
                time.sleep(1)
                self.__weibo_spider_helper(url)
                return
            else:
                print("未知错误", data)
                exit(-2)

        data = parse_weibo(data)
        ## 数据库加锁
        self.weibo_lock.acquire()
        for one in data:
            self.user_col.update({'_id': self.uid}, {'$push': {'weibo': one}})
        self.weibo_lock.release()

    def __fans_and_follow_helper(self, current_page, type):
        """type: 粉丝或者关注"""

        if type == 'follows':
            url = self.urlTool.follow_user(self.uid, current_page)
        elif type == 'fans':
            url = self.urlTool.fans_user(self.uid, current_page)
        else:
            print("人群类型参数错误")
            exit(-1)
            return

        logger.info(url)
        try:
            data = json.loads(GET(url))
        except:
            traceback.print_exc()
            self.__end_page = True
            self.__fans_and_follow_helper(current_page, type)
            return

        if data['ok'] == 0:
            if 'msg' in data and data['msg'] == '这里还没有内容':
                self.__end_page = True
                return None
            if 'msg' in data and data['msg'] == '请求过于频繁,歇歇吧':
                logger.info("线程请求频繁，开始休眠1s")
                time.sleep(1)
            else:
                print("未知错误", data)
                exit(-2)

        user_ids = parse_user(data)
        self.weibo_lock.acquire()
        for user_id in user_ids:
            self.user_col.update({'_id': self.uid}, {'$push': {type: user_id}})  # 将user追加到关注或粉丝列表
        self.weibo_lock.release()

    def join_threads(self, thread_count, thread_list, force=False):
        if thread_count % 50 == 0 or force:
            for th in thread_list:
                th.join()
                thread_list.clear()
            return 1
        return thread_count + 1

    def fans_and_follow(self):
        logger.info("flush the old fans and follows list...")
        self.user_col.update({'_id': self.uid}, {'$set': {'follows': []}})
        self.user_col.update({'_id': self.uid}, {'$set': {'fans': []}})

        thread_list = []
        for type in ['follows', 'fans']:
            logger.info('beginning download %s list' % type)
            current_page = 1
            self.__end_page = False  # 是否为最后一页数据
            while not self.__end_page:
                # 添加、执行、控制线程
                thread = threading.Thread(target=self.__fans_and_follow_helper, args=(current_page, type))
                thread.start()
                thread_list.append(thread)
                if len(thread_list) > 1000:
                    logger.info('threads up to 100, waiting for flushing...')
                    for t in thread_list:
                        t.join()
                    thread_list.clear()

                # 准备下载下一页
                current_page += 1
                time.sleep(self.frequency)
            logger.info('%s download completed!' % type)
        for t in thread_list:
            t.join()

    def weibo_blogs(self):
        # 获取用户基本信息以及该用户发布或转发的微博
        self.user_col.update({'_id': self.uid}, {'$set': {'weibo': []}})
        logger.info("开始获取微博内容")
        current_page = 1
        thread_list = []
        self.__end_page = False
        while not self.__end_page:
            url = self.urlTool.blogs_user(self.uid, current_page)
            logger.info(url)
            thread = threading.Thread(target=self.__weibo_spider_helper, args=([url]))
            thread.start()
            thread_list.append(thread)

            if len(thread_list) > 1000:
                logger.info('threads up to 100, waiting for flushing...')
                for t in thread_list:
                    t.join()
                thread_list.clear()

            current_page += 1
            time.sleep(self.frequency)
        logger.info('blog爬取完毕，等待子线程结束')
        for h in thread_list:
            h.join()


if __name__ == "__main__":
    pass
