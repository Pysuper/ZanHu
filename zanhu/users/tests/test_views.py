# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author   ：zheng xingtao

from django.test import RequestFactory
from test_plus.test import TestCase

from zanhu.users.views import UserUpdateView


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.make_user()


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        super().setUp()  # 继承父类的方法
        self.view = UserUpdateView()

        request = self.factory.get("/fake-url")
        request.user = self.user
        self.view.request = request  # 把request请求发送给视图

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), "/users/testuser/")

    def test_get_object(self):
        self.assertEqual(self.view.get_object(), self.user)
