from spider.spider import Spider
from analysis.dataView import DataView
from utils import *

if __name__ == '__main__':
    xls_gener = DataView()

    # 1. 爬取博主信息、微博发布和转发、关注博主id、被关注博主列表到数据库
    # sp = Spider(6029786152) # 获取yc的数据

    # 2. 根据uid列表生成用户基本profile信息的excel文件
    # uids = [6029786152, 5102089477]
    # path = xls_gener.profile_to_xls(uids)

    # 3. 生成一个用户所有微博到excel,返回
    # path = xls_gener.blogs_to_xls(6029786152)

    # 4. 邮件发送附件
    # MAIL('发送附件测试','605725874@qq.com', './assets/profile/profile_12-19-074734.xls')

    # 5. 生成词云
    # path = xls_gener.word_cloud(6029786152)

