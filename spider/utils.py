import requests, logging, threading
from seettings import *
from pymongo import MongoClient



def __get_logger():
    """获取logger"""
    fmt = logging.Formatter(LOG_FORMATTER, datefmt='%m-%d-%A %H:%M:%S')
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger = logging.getLogger("wbLog")
    logger.setLevel("INFO")
    logger.addHandler(console)
    return logger


def GET(url):
    """GET请求"""
    response = requests.get(url)
    return response.content.decode('utf-8')


# logger
logger = __get_logger()


# MongoDB数据库
DB = MongoClient(DB_HOST, DB_PORT)[DB_NAME]


if __name__ == '__main__':
    pass
