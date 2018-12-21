from .Spider.spider.spider import Spider
from .Spider.analysis.dataView import DataView
from .Spider.utils import *

if __name__ == '__main__':
    xls_gener = DataView()

    # # 用户功能
    # 1. 生成一个用户所有微博到excel,返回excel路径
    # 对应UserIndexInfo
    path = xls_gener.blogs_to_xls(3554683503)

    # 2. 根据uid列表生成用户基本profile信息的excel文件
    # 对应UserBaseInfo
    uids = [6029786152, 5102089477, 2988799167,3554683503]
    path = xls_gener.profile_to_xls(uids)

    # 3. 邮件发送附件
    MAIL('Weibo Spider','微博内容数据','709531006@qq.com', path)

    # 4. 生成词云，返回词云图片路径
    # 对应UserWorldCloud
    path = xls_gener.word_cloud(3554683503)

    # 5. 根据uid生成粉丝基本信息的excel
    # 对应FansInfo
    path = xls_gener.fans_profile_to_xls(3554683503)

    # 6. 根据uid生成关注用户基本信息的excel
    # 对应FansFollowingInfo
    path = xls_gener.folows_profile_to_xls(3554683503)

    # 7. 微博情感组成分析，生成统计图
    # 待定

    # 8. 生成用户报告
    # 待定