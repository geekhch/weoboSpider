from spider.url_tools import urlTools
from spider.parse_tools import *
import traceback

class spider:
    "根据功能爬去数据保存到数据库"
    urlTool = urlTools()
    weibo_lock = threading.Lock()
    max_threads = threading.BoundedSemaphore(60)  # 最大并发网络请求线程数
    user = DB.get_collection("user")

    def __producer(self, url, buffer):
        """请求某一页的所有博客文章数据，并加入到数据库"""
        try:
            data = parse_weibo(GET(url))
        except Exception as e:
            traceback.print_exc()
            print(url)
            return
        # self.max_threads.acquire()
        self.weibo_lock.acquire()
        # buffer.append(data)
        self.user.insert_many(data)
        self.weibo_lock.release()
        # self.max_threads.release()


    def __consumer(self, buffer):
        pass



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
            thread = threading.Thread(target=self.__producer, args=(url,page_datas))
            thread.start()
            handlers.append(thread)
            if i%50== 0:
                # 最大并发50个线程
                for h in handlers:
                    h.join()
                handlers.clear()
            


