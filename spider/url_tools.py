from spider.utils import DB, HOST

class urlTools:
    """构造获取数据的url"""
    userURL = HOST + "/api/container/getIndex?"
    user = DB.get_collection("user")

    def profile_user(self, uid):
        """获取某个用户基本资料接口"""
        return self.userURL + "type=uid&value=%s" % str(uid)

    def weibo_user(self, uid, page=1):
        """
        获取用户微博接口
        """
        containerid = self.user.find_one({'_id': uid}, {'weibo_api': 1})['weibo_api']
        print(containerid)
        return self.userURL + "%s&page=%d"%(containerid, page)

    def follow_user(self, uid, page=1):
        """
        获取用户微博接口
        """
        param = "containerid=231051_-_followers_-_%s&page=%d" % (str(uid), page)
        return self.userURL + param

    def fans_user(self, uid, page=1):
        """
        获取用户微博接口
        """
        param = "containerid=231051_-_fans_-_%s&since_id=%d" % (str(uid), page)
        return self.userURL + param


if __name__ == '__main__':
    object = urlTools()
    url = object.weibo_user(5102089477)
    print("weibo",url)
    print("fans",object.fans_user(5102089477))