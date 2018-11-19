import json
from spider.utils import *
from math import ceil

def parse_profile(data):
    """
    解析用户基本数据
    https://m.weibo.cn/api/container/getIndex?type=uid&value=******
    """
    data = json.loads(data)
    if data['ok'] != 1:
        logger.warning("profile数据请求有误")
        return False
    data = data['data']
    userInfo = data['userInfo']
    tabsInfo = data["tabsInfo"]['tabs']
    userObject = {'_id': userInfo['id']}  # 保存到数据库的对象
    userInfoSave = [
        'screen_name', 'statuses_count',
        'verified', 'description', 'gender',
        'urank', 'mbtype', 'avatar_hd'
    ]
    for key in userInfoSave:
        userObject[key] = userInfo[key]
    userObject['profile_api'] = "containerid=%s" % tabsInfo[0]['containerid']
    userObject['weibo_api'] = "containerid=%s" % tabsInfo[1]['containerid']
    userObject['album_api'] = "containerid=%s" % tabsInfo[2]['containerid']
    userObject['weibo'] = []
    return userObject


def parse_relations(data):
    """
    解析粉丝或关注人的uids,
    init模式获取数据总页数，方便多线程
    """
    data = json.loads(data)
    if data['ok'] != 1:
        logger.warning("relations数据请求错误")
        return False

    friends = data['data']['cards'][-1]['card_group']
    return [user['user']['id'] for user in friends]


def __parse_weibo_helper(blog):
    """（一条）博客对象"""
    blogObject = {
        'id': blog['id'],
        'date': blog['created_at'],
        'source': blog['source'],
        'reposts_count': blog['reposts_count'],
        'comments_count': blog['comments_count'],
        'attitudes_count': blog['attitudes_count'],
        'text': blog['text'],
        'repost': None
    }
    if 'retweeted_status' in blog:
        blogObject['repost'] = __parse_weibo_helper(blog['retweeted_status'])
    return blogObject


def parse_weibo(data, init=False):
    """
    init为真则返回总页数用于初始化请求任务
    否则返回对应url请求并清洗后的数据
    """
    if isinstance(data, str):
        data = json.loads(data)
    if data['ok'] != 1:
        logger.warning("weibo数据请求失败")
        return False
    if init:
        return ceil(data['data']['cardlistInfo']['total']//10)
    blogs = data['data']['cards']  # 原始博客数据
    blogObjects = []
    for blog in blogs:
        blog=blog['mblog']
        blogObject = __parse_weibo_helper(blog)
        blogObjects.append(blogObject)
    return blogObjects


def parse_follow(data):
    data = json.loads(data)


if __name__ == '__main__':
    pass