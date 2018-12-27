from ..utils import DB, HOST

class urlTools:
    """构造获取数据的url"""
    def __init__(self):
        self.userURL = HOST + "/api/container/getIndex?"
        self.user = DB.get_collection("user")

    def profile_user(self, uid):
        """获取某个用户基本资料接口"""
        return self.userURL + "type=uid&value=%s" % str(uid)

    def blogs_user(self, uid, page=1):
        """
        获取用户微博接口
        """
        containerid = self.user.find_one({'_id': uid}, {'weibo_api': 1})['weibo_api']
        return self.userURL + "%s&page=%d"%(containerid, page)


    def follow_user(self, uid, page=1):
        """
        获取用户关注博主列表接口
        """
        param = "containerid=231051_-_followers_-_%s&page=%d" % (str(uid), page)
        return self.userURL + param

    def fans_user(self, uid, page=1):
        """
        获取用户微博接口
        """
        param = "containerid=231051_-_fans_-_%s&since_id=%d" % (str(uid), page) # fans和follow翻页参数不一样
        return self.userURL + param

    def attitudes(self, mid, page):
        """
        获取微博点赞列表 (blog_id, 页码)
        """
        return "https://m.weibo.cn/api/attitudes/show?id=%s&page=%d" % (str(mid), page)



if __name__ == '__main__':
    object = urlTools()
    url = object.blogs_user(5102089477)
    print("weibo",url)
    print("fans",object.fans_user(5102089477))