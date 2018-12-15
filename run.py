from spider.spider import spider

if __name__ == '__main__':
    sp = spider()

    # 爬取博主信息、微博发布和转发、关注博主id、被关注博主列表
    # sp.weibo_spider(1700648435)
    sp.fans_and_follow(1700648435)



