import os

import requests, logging, smtplib, traceback
from .seettings import *
from pymongo import MongoClient
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def __get_logger(name='wbLog'):
    """获取logger"""
    fmt = logging.Formatter(LOG_FORMATTER, datefmt='%m-%d-%A %H:%M:%S')
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
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


def MAIL(subject, receiver, file_path):
    """发送邮件"""
    HOST = 'smtp.163.com'
    MAIL_USER = '15682177109@163.com'
    MAIL_PASS = 'SCU123scu'
    sender = MAIL_USER
    receivers = [receiver]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEMultipart()
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = "微博爬虫附件" + "<SCU Tracker>"
    message['To'] = ";".join(receivers[:1])
    message.attach(MIMEText('weibo spider附件', "HTML", 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="weibo_spider.xls"'
    message.attach(att1)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(HOST, 25)  # 25 为 SMTP 端口号
        smtpObj.login(MAIL_USER, MAIL_PASS)
        smtpObj.sendmail(sender, receivers, message.as_string())
        logger.info("邮件发送成功")
    except:
        logger.warning(subject + "   发送失败")
        logger.warning(traceback.format_exc())


class path_manager:
    ROOT = os.path.abspath('.')
    ANALYSIS = os.path.join(ROOT, 'Spider/analysis')
    ASSETS = os.path.join(ROOT, 'Spider/assets')


if __name__ == '__main__':
    pass
