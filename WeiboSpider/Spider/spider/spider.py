from WeiboSpider.Spider.spider import urlTools
import threading
import traceback


class Spider:
    "根据功能爬去数据保存到数据库"
    urlTool = urlTools()
    weibo_lock = threading.Lock()  # 数据库写入锁
    user_col = DB.get_collection("user")

    def __init__(self, uid):
        """
        一键获取用户基本信息、所有微博、关注用户uid列表、粉丝用户uid列表，保存到db
        """
        self.uid = uid
        self.urlTool = urlTools()
        self.weibo_lock = threading.Lock()  # 数据库写入锁
        self.user_col = DB.get_collection("user")
        self.__end_page = False  # 线程控制使用成员变量

        if not self.user_col.find_one({'_id': uid}):
            url = self.urlTool.profile_user(uid)
            data = parse_profile(GET(url))
            self.user_col.replace_one({'_id': uid}, data, upsert=True)  # 新增字段而不是完全替换
            self.__weibo_blogs()
            self.__fans_and_follow()



    def __weibo_spider_helper(self, url, buffer):
        """请求某一页的所有博客文章数据，并加入到数据库"""
        try:
            data = parse_weibo(GET(url))  # 一页10个微博文章
        except:
            traceback.print_exc()
            print(url)
            return

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
            exit(1)
            return
        print(url)
        data = GET(url)
        try:
            data = json.loads(data)
            # 判断是否到了尾页
            if data['ok'] == 0:
                if 'msg' in data and data['msg'] == '这里还没有内容':
                    self.__end_page = True
                    return None
                else:
                    print("未知错误", data)

            user_ids = parse_user(data)
            self.weibo_lock.acquire()
            for user_id in user_ids:
                self.user_col.update({'_id': self.uid}, {'$push': {type: user_id}})  # 将user追加到关注或粉丝列表
            self.weibo_lock.release()
        except:
            traceback.print_exc()

    def join_threads(self, thread_count, thread_list, force = False):
        if thread_count % 50 == 0 or force:
            for th in thread_list:
                th.join()
                thread_list.clear()
            return 1
        return thread_count+1

    def __fans_and_follow(self):
        self.__end_page = False  # 线程控制使用成员变量
        current_page = 1
        logger.info("开始获取关注列表")
        # 控制并发50个线程
        self.user_col.update({'_id': self.uid}, {'$set': {'follows': []}})
        self.user_col.update({'_id': self.uid}, {'$set': {'fans': []}})
        thread_count = 1
        thread_list = []
        while not self.__end_page:
            thread = threading.Thread(target=self.__fans_and_follow_helper, args=(current_page, 'follows'))
            thread.start()
            current_page += 1
            thread_list.append(thread)
            thread_count = self.join_threads(thread_count,thread_list)
        self.join_threads(0, thread_list, True)

        self.__end_page = False  # 线程控制使用成员变量
        current_page = 1
        logger.info("开始获取粉丝列表")
        # 控制并发50个线程
        thread_count = 1
        thread_list = []
        while not self.__end_page:
            thread = threading.Thread(target=self.__fans_and_follow_helper, args=(current_page,'fans'))
            thread.start()
            current_page += 1
            thread_list.append(thread)
            thread_count = self.join_threads(thread_count,thread_list)
        self.join_threads(0, thread_list, True)




    def __weibo_blogs(self):
        # 获取用户基本信息以及该用户发布或转发的微博
        url = self.urlTool.weibo_user(self.uid)
        data = GET(url)
        total_pages = parse_weibo(data, init=True)  # 获取总页数

        page_datas, handlers = [], []
        for i in range(1, total_pages):
            url = self.urlTool.weibo_user(self.uid, i)
            logger.info(url)
            thread = threading.Thread(target=self.__weibo_spider_helper, args=(url, page_datas))
            thread.start()
            handlers.append(thread)
            if i % 50 == 0:
                # 控制最大并发50个线程
                for h in handlers:
                    h.join()
                handlers.clear()


if __name__ == "__main__":
    pass
