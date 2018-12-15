from spider.url_tools import urlTools
from spider.parse_tools import *
import traceback

class spider:
    "根据功能爬去数据保存到数据库"
    urlTool = urlTools()
    weibo_lock = threading.Lock() #数据库写入锁
    user_col = DB.get_collection("user")

    def __init__(self, uid):
        self.uid = uid

        ##获取基本信息
        url = self.urlTool.profile_user(uid)
        data = parse_profile(GET(url))
        self.user_col.replace_one({'_id': uid}, data, upsert=True)  # 新增字段而不是完全替换


    def __weibo_spider_helper(self, url, buffer):
        """请求某一页的所有博客文章数据，并加入到数据库"""
        try:
            data = parse_weibo(GET(url)) #一页10个微博文章
        except:
            traceback.print_exc()
            print(url)
            return

        ## 数据库加锁
        self.weibo_lock.acquire()
        for one in data:
            self.user_col.update({'_id':self.uid}, {'$push':{'weibo':one}})
        self.weibo_lock.release()


    def __fans_and_follow_helper(self, current_page, group):
        """group: 粉丝或者关注"""
        url = urlTools.follow_user(self.uid, current_page)
        data = GET(url)
        try:
            data = json.loads(data)
            # 判断是否到了尾页
            if data['ok'] == 0:
                if data['msg'] == '这里还没有内容':
                    self.__end_page = True
                    return None
            
            users = parse_user(data)

            self.weibo_lock.acquire()
            for user in users:
                self.user_col.update({'_id':self.uid}, {'$push':{'weibo':user}}) # 将user追加到关注或粉丝列表
            self.weibo_lock.release()
        except:
            traceback.print_exc()





    def fans_and_follow(self):
        self.__end_page = False # 线程控制使用成员变量
        current_page = 1
        logger.info("开始获取关注列表")
        thread_num = 0
        while not __end_page:
            thread = threading.Thread(target=self.__fans_and_follow_helper, args=(current_page, ))
            
        raw_follow = GET(follow)



    def weibo_spider(self):
        # 获取用户基本信息以及该用户发布或转发的微博
        url = self.urlTool.weibo_user(self.uid)
        data = GET(url)
        total_pages = parse_weibo(data, init=True) # 获取总页数

        page_datas, handlers = [],[]
        for i in range(1,total_pages):
            url = self.urlTool.weibo_user(self.uid, i)
            thread = threading.Thread(target=self.__weibo_spider_helper, args=(url, page_datas))
            thread.start()
            handlers.append(thread)
            if i%50== 0:
                # 控制最大并发50个线程
                for h in handlers:
                    h.join()
                handlers.clear()


if __name__ == "__main__":
    pass
    sp = spider()
    sp.fans_and_follow(1700648435)

    
