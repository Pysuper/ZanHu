#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：test_views.py
# Author   ：zheng xingtao
# Date     ：2021/1/7 10:09

from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from zanhu.news.models import News


class NewsViewsTest(TestCase):
    def setUp(self):
        # 创建用户
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")

        # 创建用户连接
        self.client = Client()
        self.other_client = Client()

        # 用户登录
        self.client.login(username="user01", password="password")
        self.other_client.login(username="user02", password="password")

        # 用户发表动态
        self.first_news = News.objects.create(user=self.user, content="第一条动态")
        self.second_news = News.objects.create(user=self.user, content="第二条动态")

        # 用户发表评论
        self.third_news = News.objects.create(
            user=self.other_user,
            content="第一条动态的评论",
            reply=True,
            parent=self.first_news
        )

    def test_news_list(self):
        """测试动态列表页功能"""
        response = self.client.get(reverse("news:list"))
        assert response.status_code == 200
        assert self.first_news in response.context["news_list"]
        assert self.second_news in response.context["news_list"]
        assert self.third_news not in response.context["news_list"]

    def test_delete_news(self):
        """删除动态"""
        initial_count = News.objects.count()
        response = self.client.post(reverse("news:delete_news", kwargs={"pk": self.second_news.pk}))  # 删除第二条动态
        assert response.status_code == 302
        assert News.objects.count() == initial_count - 1

    def test_post_news(self):
        "发送动态"
        initial_count = News.objects.count()
        response = self.client.post(
            reverse("news:post_news"),
            {"post": "使用reverse，发送了一个Ajax的POST请求"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"  # TODO: 发送Ajax Request请求
        )
        assert response.status_code == 200
        assert News.objects.count() == initial_count + 1

    def test_like_news(self):
        """点赞"""
        response = self.client.post(
            reverse("news:like_post"),
            {"news": self.first_news.pk},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response.status_code == 200
        assert self.first_news.count_likers() == 1
        assert self.user in self.first_news.get_likers()
        assert response.json()["likes"] == 1

    def test_get_thread(self):
        """获取动态的评论"""
        response = self.client.get(
            reverse("news:get_thread"),
            {"news": self.first_news.pk},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response.status_code == 200
        assert response.json()["uuid"] == str(self.first_news.pk)
        assert "第一条动态" in response.json()["news"]
        assert "第一条动态的评论" in response.json()["thread"]

    def test_post_comments(self):
        """发表评论"""
        response = self.client.post(
            reverse("news:post_comments"),
            {"reply": "第二条动态的评论", "parent": self.second_news.pk},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response.status_code == 200
        assert response.json()["comments"] == 1
