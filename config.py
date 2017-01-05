# -*- coding:utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#跨站请求攻击保护
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

POSTS_PER_PAGE = 5

YEAR = ['2016','2015','2014','2013','2012','2011','2006-2010','2000-2005','1990-1999','before 1989']
RATE = ['9','8','7','6','5','4']
TAG = ['爱情', '喜剧', '动画', '剧情', '科幻', '动作', '经典', '悬疑', '青春', '犯罪', '惊悚', '文艺',
        '纪录片', '励志', '恐怖', '战争', '短片', '黑色幽默', '魔幻', '传记', '情色',  '暴力', '动画短片',
       '家庭', '音乐', '童年', '浪漫', '黑帮', '女性', '同志', '烂片', 'cult']
COUNTRY = [u'\u5370\u5ea6', u'\u6fb3\u5927\u5229\u4e9a', u'\u6cf0\u56fd', u'\u897f\u73ed\u7259', u'\u610f\u5927\u5229', u'\u52a0\u62ff\u5927', u'\u5fb7\u56fd', u'\u53f0\u6e7e', u'\u97e9\u56fd', u'\u6cd5\u56fd', u'\u9999\u6e2f', u'\u82f1\u56fd', u'\u4e2d\u56fd\u5927\u9646', u'\u65e5\u672c']


