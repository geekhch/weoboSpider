from spider.url_tools import urlTools
from spider.parse_tools import *

class spider():
    "根据功能爬去数据保存到数据库"
    urlTool = urlTools()
    weibo_lock = threading.Lock()
    max_threads = threading.BoundedSemaphore(60)  # 最大并发网络请求线程数
    user = DB.get_collection("user")

    def __producer(self, url, buffer):
        """网络请求数据"""
        data = GET(url)
        self.max_threads.acquire()
        self.weibo_lock.acquire()
        buffer.append(data)
        self.weibo_lock.release()
        self.max_threads.release()
    def __consumer(self, buffer):
        while True:


    def __profile_spider(self, uid):
        url = self.urlTool.profile_user(uid)
        data = parse_profile(GET(url))
        self.user.replace_one({'_id':uid},data,upsert=True)  # 替换或新增


    def weibo_spider(self, uid):
        self.__profile_spider(uid)
        url = self.urlTool.weibo_user(uid)
        data = GET(url)
        total = parse_weibo(data, init=True)
        page_datas, handlers = [],[]
        for i in range(1,total):
            url = self.urlTool.weibo_user(uid, i)
            thread = threading.Thread(target=self.__thread, args=(url,page_datas))
            thread.start()
            handlers.append(thread)



