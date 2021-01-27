# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author   ：zheng xingtao

# 编写URL的测试用例
"""
from django.urls import reverse, resolve
from test_plus.test import TestCase


class TestUserURLs(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test_detail_reverse(self):
        # reverse: 将URL路由的名字 解析成 字符串的URL地址
        self.assertEqual(reverse("users:detail", kwargs={"username": "testuser"}), "/users/testuser/")

    def test_detail_resolve(self):
        # 反向解析
        self.assertEqual(resolve("/users/testuser/").view_name, "users:detail")

    def test_update_reverse(self):
        self.assertEqual(reverse("users:update"), "/users/update/")

    def test_update_resolve(self):
        self.assertEqual(resolve("/users/update/").view_name, "users:update")

"""
