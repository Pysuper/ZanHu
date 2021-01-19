#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：urls.py
# Author   ：zheng xingtao
# Date     ：2021/1/12 16:39

from django.urls import path

from zanhu.qa import views

app_name = "qa"

urlpatterns = [
    path("indexed/", views.QuestionListView.as_view(), name="all_q"),
    path("answered/", views.AnsweredQuestionListView.as_view(), name="answered_q"),
    path("unanswered/", views.UnansweredQuestionListView.as_view(), name="unanswered_q"),
]

