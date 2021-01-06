# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author   ：zheng xingtao


import uuid

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class News(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name="publisher", verbose_name="用户")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="thread", verbose_name="自关联")
    content = models.TextField(verbose_name="动态内容")
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_news", verbose_name="点赞用户")
    reply = models.BooleanField(default=False, verbose_name="是否未评论")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = verbose_name = "首页"

    def __str__(self):
        return self.content

    def switch_like(self, user):
        """点赞/取消点赞, 这里的动作是由某一个用户去执行的"""
        if user in self.liked.all():    # self.liked.all()==> 所有赞过的用户
            # 如果用户已经赞过，则取消赞
            self.liked.remover(user)
        else:
            # 如果用户没有赞过，则添加赞
            self.liked.add(user)

    def get_parent(self):
        """返回自关联中的上级记录或者本身"""
        if self.parent:
            return self.parent
        else:
            return self

    def reply_this(self, user, text):
        """
        回复首页的动态
        :param user: 登录的用户
        :param text: 回复的内容
        :return: None
        """
        parent = self.get_parent()  # 获取当前的父记录
        News.objects.create(
            user=user,
            content=text,
            reply=True,
            parent=parent
        )

    def get_thread(self):
        """关联到当前记录的所有记录"""
        parent = self.get_parent()
        return parent.thread.all()  # 通过related_name, 获取所有记录

    def comment_count(self):
        """评论数"""
        return self.get_thread().count()

    def count_likers(self):
        """点赞数"""
        return self.liked.count()

    def get_likers(self):
        """获取都有点赞用户"""
        return self.liked.all()
