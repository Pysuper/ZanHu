#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：views.py
# Author   ：zheng xingtao
# Date     ：2021/1/12 16:39


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from zanhu.articles.forms import ArticleForm
from zanhu.articles.models import Article
from zanhu.utils.helper import AuthorRequiredMixin


class ArticleListView(LoginRequiredMixin, ListView):
    """已发布的用户列表"""
    model = Article  # 关联的模型类
    paginate_by = 10  # 分页展示
    context_object_name = "articles"  # 上下文的名字
    template_name = 'articles/article_list.html'  # 模板文件

    def get_context_data(self, *, object_list=None, **kwargs):
        """右侧添加了标签云==>需要添加额外的上下文"""
        context = super().get_context_data()  # 重载父类方法
        context["popular_tags"] = Article.objects.get_counted_tags()  # 返回每一个标签，以及每个标签的数量
        return context

    def get_queryset(self):
        """只返回已发布的文章"""
        return Article.objects.get_published()  # 直接调用模型类中定义的方法


class DraftListView(ArticleListView):
    """草稿箱列表"""

    def get_queryset(self):
        """当前用户的草稿"""
        return Article.objects.filter(user=self.request.user).get_drafts()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """发表文章==>填写表单==>使用form"""
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_create.html"
    message = "您的文章已创建成功！"

    # initial = {"title": "OK!"}  # 在模板中自动填充的内容

    # prefix = "zheng"  # 修改表单中的id名

    def form_valid(self, form):
        form.instance.user = self.request.user  # 把登录的用户传递给表单实例
        return super().form_valid(form)

    def get_success_url(self):
        """创建成功后跳转的页面==>详情页"""
        messages.success(self.request, self.message)  # 消息传递给下一次请求
        return reverse_lazy("articles:list")

    def get_initial(self):
        """动态自动填写，重写父类方法"""
        initial = super().get_initial()
        '''
        在这里写动态填充的业务逻辑==>定期发表一些公告之类的功能
        '''
        return initial


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """文章详情"""
    model = Article
    template_name = "articles/article_detail.html"


class ArticleEditView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """编辑文章"""
    model = Article
    message = "你的文章编辑成功！"
    form_class = ArticleForm
    template_name = "articles/article_update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """创建成功后跳转的页面==>详情页"""
        messages.success(self.request, self.message)  # 消息传递给下一次请求
        return reverse_lazy("articles:article", kwargs={"slug": self.get_object().slug})
