from WeiboSpider.Spider.utils import  *
from WeiboSpider.Spider.spider.spider import Spider
import pandas as pd
import time, jieba
from wordcloud import WordCloud

class DataView:
    def __init__(self):
        # 数据库集合
        self.user_col = DB.get_collection("user")

    def word_cloud(self, uid):
        '''返回生成的词云图片的路径'''
        wc = WordCloud(
            background_color="white",  # 设置背景颜色
            max_words=200,  # 设置最大显示的词云数
            font_path='C:\\Windows\\Fonts\\STXINGKA.TTF',  # 这种字体都在电脑字体中，一般路径
            height=1200,
            width=1600,
            max_font_size=150,
            random_state=30
        )
        texts = ""
        blogs = self.user_col.find_one({'_id': uid},{'weibo':True, '_id':False})['weibo']
        for blog in blogs:
            texts += blog['text']
        wcf = wc.generate(texts)
        path = './assets/word_clouds/%s.png' % str(uid)
        wcf.to_file(path)
        return path


    def blogs_to_xls(self, uid):
        """
        功能：将uid对应用户所有微博文字内容及其分词写入excel
        返回：excel文件的路径
        """
        blogs_data = {}
        info = ['id', 'date', 'source', 'reposts_count', 'comments_count', 'attitudes_count', 'text', 'text_cut']
        for k in info:
            blogs_data[k] = []

        blogs = self.user_col.find_one({'_id': uid},{'weibo':True, '_id':False})['weibo']
        for blog in blogs:
            blog['text_cut'] = list(jieba.cut(blog['text']))
            for k in info:
                blogs_data[k].append(blog[k])
        blogs_pd = pd.DataFrame(blogs_data)
        path = './assets/blogs/blogs_%s.xls' % str(uid)
        blogs_pd.to_excel(path)
        return path


    def profile_to_xls(self, uids):
        """
        功能：通过uid列表生成用户基本资料(profile)清单
        返回：生成excel的文件相对路径
        """
        profile_data = {}
        info = ['_id', 'screen_name', 'statuses_count', 'verified', 'description', 'gender', 'urank', 'mbtype', 'avatar_hd']
        for k in info:
            profile_data[k] = []
        for uid in uids:
            Spider(uid)
            user_profile = self.user_col.find_one({'_id':uid})
            for k in info:
                profile_data[k].append(user_profile[k])

        profile_pd = pd.DataFrame(profile_data)
        path = './assets/profile/profile_%s.xls' % time.strftime('%m-%d-%H%M%S')
        profile_pd.to_excel(path)
        return path



