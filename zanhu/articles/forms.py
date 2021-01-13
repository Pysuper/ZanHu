#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：froms.py
# Author   ：zheng xingtao
# Date     ：2021/1/13 11:21

from django import forms
from markdownx.fields import MarkdownxFormField

from zanhu.articles.models import Article


class ArticleForm(forms.ModelForm):
    """用户发表文章的表单"""
    edited = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)  # initial初始化值,required用户可以不填写
    status = forms.CharField(widget=forms.HiddenInput())  # 对用户不可见
    content = MarkdownxFormField()

    class Meta:
        model = Article
        fields = ["title", "content", "image", "tags"]
