#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：urls.py
# Author   ：zheng xingtao
# Date     ：2021/1/12 16:39

from django.urls import path

# 配置视图缓存：缓存视图中的所有数据
from django.views.decorators.cache import cache_page
from zanhu.articles import views

app_name = "articles"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("write-new-article/", views.ArticleCreateView.as_view(), name="write_new"),
    path("drafts/", views.DraftListView.as_view(), name="drafts"),

    # 在这里配置对于试图的缓存--缓存5分钟
    path("<str:slug>/", cache_page(5 * 60)(views.ArticleDetailView.as_view()), name="article"),
    path("edit/<int:pk>/", views.ArticleEditView.as_view(), name="edit_article"),
]
