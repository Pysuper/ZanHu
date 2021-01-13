#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：urls.py
# Author   ：zheng xingtao
# Date     ：2021/1/12 16:39

from django.urls import path

from zanhu.articles import views

app_name = "articles"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("write-new-article/", views.ArticleCreateView.as_view(), name="write_new"),
    path("drafts/", views.DraftListView.as_view(), name="drafts"),
]
