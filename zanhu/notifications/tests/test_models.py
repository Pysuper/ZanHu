#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：test_models.py
# Author   ：zheng xingtao
# Date     ：2021/1/7 10:08

from test_plus.test import TestCase

from zanhu.news.models import News


class NewsTest(TestCase):
    def setUp(self):
        # 创建两个用户，每个用户发表一条动态
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.first_news = News.objects.create(user=self.user, content="用户user01的第一条动态")
        self.second_news = News.objects.create(user=self.user, content="用户user01的第二条动态")
        self.third_news = News.objects.create(
            user=self.other_user,
            content="用户02对第一条动态的评论",
            reply=True,
            parent=self.first_news
        )

    def test__str__(self):
        self.assertEqual(self.first_news.__str__(), "用户user01的第一条动态")

    def test_switch_liked(self):
        "测试点赞或者取消赞"
        self.first_news.switch_like(self.user)
        assert self.first_news.count_likers() == 1
        assert self.user in self.first_news.get_likers()

    def test_reply_this(self):
        "测试回复功能"
        initial_count = News.objects.count()
        self.first_news.reply_this(self.other_user, "用户02对第一条动态的评论")
        assert News.objects.count() == initial_count + 1
        assert self.first_news.comment_count() == 2
        assert self.third_news in self.first_news.get_thread()
