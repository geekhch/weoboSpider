from ..utils import *
from ..spider.spider import Spider
import pandas as pd
import time, json, cv2, re, jieba
from jieba import posseg
import thulac
from wordcloud import WordCloud


class DataView:
    def __init__(self):
        # 数据库集合
        self.user_col = DB.get_collection("user")

    def __cut(self, text_list):
        t = thulac.thulac()
        for sentence in text_list:
            for pair in t.cut(sentence):
                yield pair

    def word_cloud(self, uid, color='black'):
        """返回生成的词云图片的路径"""
        wc = WordCloud(
            background_color=color,  # 设置背景颜色
            # max_words=500,  # 设置最大显示的词云数 #simfang.ttf
            font_path='C:\\Windows\\Fonts\\simfang.ttf',  # 这种字体都在电脑字体中，一般路径
            # font_path = '/System/Library/Fonts/PingFang.ttc',
            mask=cv2.imread(path_manager.ANALYSIS + '/temp/merry.jpg'),
            random_state=30,
        )

        # 提取博文并去掉HTML标签
        texts = ""
        test = self.user_col.find_one({'_id': uid}, {'weibo': True, '_id': False})
        if not test or not test['weibo']:
            Spider(uid, blogs=True, fans_follow=False)
        blogs = self.user_col.find_one({'_id': uid}, {'weibo': True, '_id': False})['weibo']
        for blog in blogs:
            texts += blog['text']
        texts = re.sub(r'<.*?>', '。', texts)
        texts = texts.split('。')

        # jieba分词、去停用词、统计词频
        # jieba.add_word('微博')
        # jieba.add_word('王一博')
        # jieba.add_word('肖战')
        # stopw = json.load(open(path_manager.ANALYSIS + '/stop_words.json', encoding='utf8'))  # 加载停用词
        # words_flag = posseg.cut(texts)
        # word_frequence = {}
        # for w in words_flag:
        #     if not w.word in stopw and not w.flag in ['w', 'c', 'y','o', 'zg', 'd'] and len(w.word)>1:
        #         if w.word in word_frequence:
        #             word_frequence[w.word] += 1
        #         else:
        #             word_frequence[w.word] = 1
        # if len(word_frequence)<1:
        #     print("该用户没有发布微博！")
        #     return None

        # thulac分词
        # t = thulac.thulac()
        stopw = json.load(open(path_manager.ANALYSIS + '/stop_words.json', encoding='utf8'))  # 加载停用词

        print('开始分词')
        # words_flag = t.cut(texts)
        # print('分词结束')
        word_frequence = {}
        for w,f in self.__cut(texts):
            if not w in stopw and not f in ['w', 'c', 'y']: # and len(w)>1:
                if w in word_frequence:
                    word_frequence[w] += 1
                else:
                    word_frequence[w] = 1
        if len(word_frequence)<1:
            print("该用户没有发布微博！")
            return None

        wcf = wc.generate_from_frequencies(word_frequence)
        path = path_manager.ASSETS + '/word_clouds/cloud_%s_%s.png' % (time.strftime('%m-%d-%H%M%S'),str(uid))
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

        test = self.user_col.find_one({'_id': uid}, {'weibo': True, '_id': False})
        if not test or not test['weibo']:
            Spider(uid)
        blogs = self.user_col.find_one({'_id': uid}, {'weibo': True, '_id': False})['weibo']

        for blog in blogs:
            blog['text_cut'] = list(jieba.cut(blog['text']))
            for k in info:
                blogs_data[k].append(blog[k])
        blogs_pd = pd.DataFrame(blogs_data)
        path = path_manager.ASSETS + '/blogs/blogs_%s_%s.xls' % ( time.strftime('%m-%d-%H%M%S'),str(uid))
        blogs_pd.to_excel(path)
        return path

    def profile_to_xls(self, uids, path=None):
        """
        功能：通过uid列表生成用户基本资料(profile)清单
        返回：生成excel的文件相对路径
        """
        profile_data = {}
        info = ['_id', 'screen_name', 'statuses_count', 'verified', 'description', 'gender', 'urank', 'mbtype',
                'avatar_hd']
        for k in info:
            profile_data[k] = []
        for uid in uids:
            if not self.user_col.find_one({'_id':uid}):
                Spider(uid, False, False)
            user_profile = self.user_col.find_one({'_id': uid})
            for k in info:
                profile_data[k].append(user_profile[k])

        profile_pd = pd.DataFrame(profile_data)
        if path is None:
            path = path_manager.ASSETS + '/profile/profile_%s.xls' % time.strftime('%m-%d-%H%M%S')
        profile_pd.to_excel(path)
        return path

    def fans_profile_to_xls(self, uid):
        """将用户的粉丝和关注者基本信息生成excel"""
        test = self.user_col.find_one({'_id': uid}, {'fans': True, '_id': False})
        if not test or not test['fans']:
            Spider(uid)
        user_list = self.user_col.find_one({'_id':uid},{'fans':True})
        path = path_manager.ASSETS + '/fans/fans_%s_%s.xls' %(time.strftime('%m-%d-%H%M%S'),str(uid))
        return self.profile_to_xls(user_list['fans'], path)

    def folows_profile_to_xls(self, uid):
        """将用户的粉丝和关注者基本信息生成excel"""
        test = self.user_col.find_one({'_id': uid}, {'follows': True, '_id': False})
        if not test or not test['follows']:
            Spider(uid)
        user_list = self.user_col.find_one({'_id':uid},{'follows':True})
        path = path_manager.ASSETS + '/follows/follows_%s_%s.xls' %(time.strftime('%m-%d-%H%M%S'),str(uid))
        return self.profile_to_xls(user_list['follows'], path)
