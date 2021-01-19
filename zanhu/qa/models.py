# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author   ：zheng xingtao
import uuid
from collections import Counter

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from slugify import slugify
from taggit.managers import TaggableManager


class Vote(models.Model):
    """# 通用模型类：使用Django中的ContentType, 同时关联用户对问题和回答的投票"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="qa_vote", on_delete=models.CASCADE, verbose_name="用户")
    value = models.BooleanField(default=True, verbose_name="赞同或反对")  # True-赞同，False-反对

    # GenericForeignKey设置
    content_type = models.ForeignKey(ContentType, related_name="votes_on", on_delete=models.CASCADE)

    # 这里指的是其他模型类的ID，注意类型使用
    object_id = models.CharField(max_length=255)
    vote = GenericForeignKey("content_type", "object_id")  # 等同于GenericForeignKey()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = verbose_name_plural = "投票"
        unique_together = ("user", "content_type", "object_id")  # 约束条件，联合唯一键
        # SQL优化-索引
        index_together = ("content_type", "object_id")  # 联合唯一索引


class QuestionQuerySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_answered(self):
        """已有答案的问题"""
        return self.filter(has_answer=True)

    def get_unanswered(self):
        """未被回答的问题"""
        return self.filter(has_answer=False)

    def get_counted_tags(self):
        """统计所有已发表的问题中，每一个标签的数量(大于0的)"""
        tag_dict = {}
        query = self.all().annotate(tagged=models.Count('tags')).filter(tags__gt=0)  # TODO: 聚合分组
        for obj in query:
            for tag in obj.tag.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Question(models.Model):
    """
    自动生成slug、tag管理 ==> python-slugify、django-taggit
    """
    STATUS = (("O", "Open"), ("C", "Close"), ("D", "Draft"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="q_author", verbose_name="提问者")
    title = models.CharField(max_length=255, unique=True, verbose_name="标题")
    slug = models.SlugField(max_length=80, null=True, blank=True, verbose_name="(URL)别名")
    status = models.CharField(max_length=1, choices=STATUS, default="O", verbose_name="问题状态")  # 默认开放
    content = MarkdownxField(verbose_name="内容")
    tags = TaggableManager(help_text="多个标签使用,（英文）隔开", verbose_name="标签")
    has_answer = models.BooleanField(default=False, verbose_name="接受回答")  # 当前问题是否有接受的答案
    votes = GenericRelation(Vote, verbose_name="投票情况")  # 通过GenericRelation关联到Vote表，不是实际的字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    objects = QuestionQuerySet.as_manager()  # TODO: 关联自定义的查询集

    class Meta:
        ordering = ("-created_at",)
        verbose_name = verbose_name_plural = "问题"

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """保存的时候，自动生成slug标签"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """得票数：赞-踩"""
        # TODO: 这里的写法！！！
        dic = Counter(self.votes.objects.values_list('value', flat=True))  # 统计得票数
        return dic[True] - dic[False]

    def get_answers(self):
        """获取问题的所有回答"""
        return Answer.objects.filter(question=self)  # self作为参数，返回当前的问题

    def count_answers(self):
        """显示问题下面有多少个回答"""
        return self.get_answers().count()

    def get_upvoters(self):
        """用列表生成式，获取赞同的用户、反对的用户"""
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        """用列表生成式，获取赞同的用户、反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False)]

    def get_accepted_answer(self):
        """当前问题中，被接受的回答"""
        return Answer.objects.get(question=self, is_answer=True)


class Answer(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="a_author", on_delete=models.CASCADE, verbose_name="回答者")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题")
    content = MarkdownxField(verbose_name="内容")
    is_answer = models.BooleanField(default=False, verbose_name="回答是否被接受")
    votes = GenericRelation(Vote, verbose_name="投票情况")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ("-is_answer", "-created_at")
        verbose_name = verbose_name_plural = "回答"

    def __str__(self):
        return self.content

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """得票数：赞-踩"""
        # TODO: 这里的写法！！！
        dic = Counter(self.votes.objects.values_list('value', flat=True))  # 统计得票数
        return dic[True] - dic[False]

    def get_downvoters(self):
        """用列表生成式，获取赞同的用户、反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False)]

    def get_accepted_answer(self):
        """当前问题中，被接受的回答"""
        return Answer.objects.get(question=self, is_answer=True)

    def accept_answer(self):
        """接受回答"""

        # 便于代码扩展
        # 对于需要返回查询集的--写在QuerySetModel中
        # 模型类中数据库处理的--写在Models中
        # 业务相关逻辑的处理---写在Views中

        # 当一个问题有多个回答的时候，只能采纳一个回答，其他一律设置为未接收
        answer_set = Answer.objects.filter(question=self.question)  # 查询当前问题的所有回答
        answer_set.update(is_answer=False)  # 将所有回答一律置为未接收

        # 接受当前回答并保存
        self.is_answer = True
        self.save()

        # 该问题已有被接受的回答，保存
        self.question.has_answer = True
        self.question.save()
