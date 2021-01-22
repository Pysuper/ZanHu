#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：views.py
# Author   ：zheng xingtao
# Date     ：2021/1/12 16:39


from django.contrib import messages  # Django消息框架
from django.contrib.auth.decorators import login_required  # 装饰函数 的登录装饰器
from django.contrib.auth.mixins import LoginRequiredMixin  # 被类继承 的登录装饰器
from django.core.exceptions import PermissionDenied  # 异常处理
from django.http import JsonResponse
from django.urls import reverse_lazy  # URL的反向解析：reverse-反向解析，resolve-正向解析
from django.views.decorators.http import require_http_methods  # 装饰http请求方法的函数
from django.views.generic import CreateView, ListView, DetailView  # 通用类视图

from zanhu.qa.forms import QuestionForm
from zanhu.qa.models import Question, Answer
from zanhu.utils.helper import ajax_required  # 自定义的ajax校验


class QuestionListView(LoginRequiredMixin, ListView):
    """所有问题页"""
    model = Question
    paginate_by = 10
    context_object_name = "questions"
    template_name = "qa/question_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tags()  # 页面标签功能
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


class CreateQuestionView(LoginRequiredMixin, CreateView):
    """用户提问"""
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    message = "问题已提交！"

    def form_valid(self, form):
        # form表单验证
        form.instance.user = self.request.user
        return super(CreateQuestionView, self).form_valid(form)

    def get_success_url(self):
        # 提交之后跳转的url
        messages.success(self.request, self.message)
        return reverse_lazy("qa:unanswered_q")


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """问题详情页"""
    model = Question
    # 这里的后面两个，可以不写，使用Django DetailView中默认的，但是前端模板文件中一定要给成一样的
    context_object_name = "question"
    template_name = "qa/question_detail.html"


class CreateAnswerView(LoginRequiredMixin, CreateView):
    """回答问题"""
    model = Answer
    fields = ["content", ]
    message = "您的问题已提交！"
    template_name = "qa/answer_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs["question_id"]
        return super(CreateAnswerView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("qa:question_detail", kwargs={"pk": self.kwargs["question_id"]})


@login_required
@ajax_required
@require_http_methods(["POST"])
def question_vote(request):
    """给问题投票，Ajax Post 请求"""
    question_id = request.POST["question"]
    value = True if request.POST["value"] == 'U' else False  # U--赞，D--踩
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)  # TODO: 当前问题的所有投票用户--通用外键

    # 下面是用户对于点赞和踩的几种操作可能
    '''
    # 1. 用户首次操作，点赞/踩
    if request.user.pk not in users:
        question.votes.create(user=request.user, value=value)

    # 2. 用户已经赞过，要取消赞/踩一下
    elif question.votes.get(user=request.user).value:
        if value:
            question.votes.get(user=request.user).delete()
        else:
            question.votes.update(user=request.user, value=value)

    # 3. 用户已经踩过，要取消踩/赞一下
    else:
        if not value:
            question.votes.get(user=request.user).delete()
        else:
            question.votes.update(users=request.user, value=value)
    '''

    # TODO: 优化 ==> 使用update_or_create() ==> 如果有则更新，没有则创建
    if request.user.pk in users and (question.votes.get(user=request.user).value == value):
        # 删除
        # 1. 用户已经再赞过/踩过的列表里
        # 2. 如果当前数据库中的状态为，赞，，，前端再发一个 赞 ==> 也就是取消的操作
        question.votes.get(user=request.user).delete()
    else:
        # 要么更新；要么创建
        question.votes.update_or_create(user=request.user, defaults={"value": value})

    return JsonResponse({"votes": question.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def answer_vote(request):
    """给回答投票，Ajax Post 请求"""
    answer_id = request.POST["answer"]
    value = True if request.POST["value"] == 'U' else False  # U--赞，D--踩
    answer = Answer.objects.get(uuid_id=answer_id)
    users = answer.votes.values_list('user', flat=True)

    if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})

    return JsonResponse({"votes": answer.total_votes()})


@login_required
@ajax_required
@require_http_methods(["POST"])
def accept_answer(request):
    """
    接受回答，Ajax Post 请求
    已经被接受的答案用户不能取消
    """
    answer_id = request.POST["answer"]
    answer = Answer.objects.get(uuid_id=answer_id)

    # 如果当前登录用户不是提问者，抛出拒绝错误
    if answer.question.user.username != request.user.username:
        raise PermissionDenied

    answer.accept_answer()
    return JsonResponse({"status": "true"})
