#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：test_views.py
# Author   ：zheng xingtao
# Date     ：2021/1/15 15:45

import tempfile

from PIL import Image
from django.test import override_settings
from test_plus.test import TestCase


class ArticleViewTest(TestCase):
    @staticmethod
    def get_temp_img():
        """创建并读取临时图片文件"""
        size = (200, 200)
        color = (255, 0, 0, 0)

        # 这里是使用上下文管理器，保存处理文件的方法
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            image = Image.new("RGB", size, color)
            image.save(f, "PNG")
        return open(f.name, mode="rb")

    def setUp(self):
        """初始化操作"""
        pass
        self.test_image = self.get_temp_img()

    def tearDown(self):
        """测试结束时，关闭临时文件"""
        self.test_image.close()

    def test_index_articles(self):
        """测试文章列表页"""
        pass

    def test_error_404(self):
        """访问一篇不存在的文章"""
        pass

    # 使用装饰器的方式，修改当前测试环境中静态文件所处的位置
    # 这样在测试用例中，就不会真的生成一张图片保存到media文件夹中了
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_create_article(self):
        """文章创建成功后跳转"""
        pass

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_draft_article(self):
        """测试草稿箱功能"""
        pass
