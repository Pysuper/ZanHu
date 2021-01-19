#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：views.py
# Author   ：zheng xingtao
# Date     ：2021/1/12 16:39


from django.urls import reverse_lazy    # URL的反向解析：reverse-反向解析，resolve-正向解析
from django.contrib import messages # Django消息框架
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied # 异常处理
from django.contrib.auth.decorators import login_required   # 装饰函数 的登录装饰器
from django.contrib.auth.mixins import LoginRequiredMixin   # 被类继承 的登录装饰器
from django.views.decorators.http import require_http_methods   # 装饰http请求方法的函数
from django.views.generic import CreateView, ListView, DetailView   # 通用类视图
from zanhu.utils.helper import ajax_required    # 自定义的ajax校验
from zanhu.qa.models import Question, Answer


class QuestionListView(LoginRequiredMixin, ListView):
    """所有问题页"""
    model = Question
    paginate_by = 10
    context_object_name =  "questions"
    template_name = "qa/question_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()   # 页面标签功能
        context["active"] = "all"
        return context


class AnsweredQuestionListView(QuestionListView):
    """已有采纳答案的问题"""
    def get_queryset(self):
        # 使用自定义查询集
        return Question.objects.get_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AnsweredQuestionListView, self).get_context_data()
        context["active"] = "answered"
        return context


class UnansweredQuestionListView(QuestionListView):
    """已有采纳答案的问题"""
    def get_queryset(self):
        # 使用自定义查询集
        return Question.objects.get_unanswered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UnansweredQuestionListView, self).get_context_data()
        context["active"] = "unanswered"
        return context

















