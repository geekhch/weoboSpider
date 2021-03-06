import json
from ..utils import *
from math import ceil  # 向上取整

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
    userObject['fans'] = []
    userObject['follows'] = []
    return userObject


def __parse_weibo_helper(blog):
    """（一条）博客对象"""
    blogObject = {
        'id': blog['id'],
        'uid': blog['user']['id'],
        'date': blog['created_at'],
        'source': blog['source'],
        'reposts_count': blog['reposts_count'],
        'comments_count': blog['comments_count'],
        'attitudes_count': blog['attitudes_count'],
        'text': blog['text'],
        'pics': [],
        'attitudes': [],
        'page_info': None
    }

    # 地理位置信息
    if 'page_info' in blog:
        blogObject['page_info'] = [
            blog['page_info']['page_title'],
            blog['page_info']['page_url']
        ]

    # blog照片
    if 'pics' in blog:
        for pic in blog['pics']:
            blogObject['pics'].append(pic['large']['url'])
    if 'retweeted_status' in blog:
        # 递归调用获取转发
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
        return []
    if 'itemid' in data and not data['itemid']:
        logger.warning('itemid为空，放弃该数据')
        return []
    if init:
        return ceil(data['data']['cardlistInfo']['total']//10)
    blogs = data['data']['cards']  # 原始博客数据
    blogObjects = []
    for blog in blogs:
        if not 'mblog' in blog:
            logger.warning('无效blog对象')
            print(blog)
            continue
        blog=blog['mblog']
        blogObject = __parse_weibo_helper(blog)
        blogObjects.append(blogObject)
    return blogObjects


def parse_user(data):
    cards = data['data']['cards']
    user_ids = []
    for card in cards:
        if card['itemid']:
            # print(card)
            try:
                for group in card['card_group']:
                    user_ids.append(group['user']['id'])
            except:
                print(card)
    return user_ids
    

if __name__ == '__main__':
    pass
