import requests, logging, threading,smtplib
from seettings import *
from pymongo import MongoClient
from email.mime.text import MIMEText
from email.header import Header


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


def MAIL(subject, message):
    """发送邮件"""
    HOST = 'smtp.163.com'
    MAIL_USER = '15682177109@163.com'
    MAIL_PASS = 'SCU123scu'
    sender = MAIL_USER
    receivers = self.collection.find_one({'_id':'information'},{'receivers':1,'_id':0})['receivers']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText(message, "HTML", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] =  "教务处通知"+"<SCU Tracker>"
    message['To'] = ";".join(receivers[:1])
    message['Cc'] = ";".join(receivers[1:])
    # 
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(HOST, 25)    # 25 为 SMTP 端口号
        smtpObj.login(MAIL_USER,MAIL_PASS)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        self.logger.info("邮件发送成功")
    except:
        self.logger.warning(subject+"   发送失败")
        self.logger.warning(traceback.format_exc())

if __name__ == '__main__':
    pass
