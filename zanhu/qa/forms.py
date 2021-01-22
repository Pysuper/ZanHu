#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：froms.py
# Author   ：zheng xingtao
# Date     ：2021/1/13 11:21

from django import forms
from markdownx.fields import MarkdownxFormField

from zanhu.qa.models import Question


class QuestionForm(forms.ModelForm):
    """用户提出问题的表单"""
    status = forms.CharField(widget=forms.HiddenInput())  # 对用户不可见
    content = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ["title", "content", "tags", "status"]
