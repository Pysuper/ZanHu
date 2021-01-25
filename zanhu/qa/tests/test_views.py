#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：test_views.py
# Author   ：zheng xingtao
# Date     ：2021/1/15 15:45

'''
# TODO： 使用TestCase做测试

from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from zanhu.qa.models import Question, Answer


class QAViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="user01", password="password")
        self.other_client.login(username="user02", password="password")
        self.question_one = Question.objects.create(
            user=self.user,
            title="问题1",
            content="问题1的内容",
            tags="测试1, 测试2"
        )
        self.question_two = Question.objects.create(
            user=self.user,
            title="问题2",
            content="问题2的内容",
            has_answer=True,
            tags="测试1, 测试2"
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question_two,
            content="问题2被采纳的回答",
            is_answer=True
        )

    def test_index_questions(self):
        response = self.client.get(reverse("qa:all_q"))
        assert response.status_code == 200
        assert "问题1" in str(response.context["questions"])

    def test_create_question_view(self):
        current_count = Question.objects.count()
        response = self.client.post(reverse("qa:ask_question"),
                                    {"title": "问题标题",
                                     "content": "问题内容",
                                     "status": "O",
                                     "tags": "测试标签"})
        assert response.status_code == 302
        new_question = Question.objects.first()
        assert new_question.title == "问题标题"
        assert Question.objects.count() == current_count + 1

    def test_answered_questions(self):
        response = self.client.get(reverse("qa:answered_q"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("问题2" in str(response.context["questions"]))

    def test_unanswered_questions(self):
        response = self.client.get(reverse("qa:unanswered_q"))
        assert response.status_code == 200
        assert "问题1" in str(response.context["questions"])

    def test_answer_question(self):
        current_answer_count = Answer.objects.count()
        response = self.client.post(
            reverse("qa:propose_answer", kwargs={"question_id": self.question_one.id}), {"content": "问题1的回答"}
        )
        assert response.status_code == 302
        assert Answer.objects.count() == current_answer_count + 1

    def test_question_upvote(self):
        """赞同问题"""
        response_one = self.client.post(
            reverse("qa:question_vote"),
            {"value": "U", "question": self.question_one.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        assert response_one.status_code == 200

    def test_question_downvote(self):
        """反对问题"""
        response_one = self.client.post(
            reverse("qa:question_vote"),
            {"value": "D", "question": self.question_one.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_answer_upvote(self):
        """赞同回答"""
        response_one = self.client.post(
            reverse("qa:answer_vote"),
            {"value": "U", "answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_answer_downvote(self):
        """反对回答"""
        response_one = self.client.post(
            reverse("qa:answer_vote"),
            {"value": "D", "answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_accept_answer(self):
        """接受回答"""
        response_one = self.client.post(
            reverse("qa:accept_answer"),
            {"answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200
'''

import json

from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from test_plus.test import CBVTestCase

from zanhu.qa import views
from zanhu.qa.models import Question, Answer


class BaseQATest(CBVTestCase):

    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.question_one = Question.objects.create(user=self.user, title="问题1", content="问题1的内容", tags="测试1, 测试2")
        self.question_two = Question.objects.create(user=self.user, title="问题2", content="问题2的内容", has_answer=True, tags="测试1, 测试2")
        self.answer = Answer.objects.create(user=self.user, question=self.question_two, content="问题2被采纳的回答", is_answer=True)

        # 使用 RequestFactory 生成一个get请求, 不经过路由，直接将请求发送到视图中
        self.request = RequestFactory().get('/fake-url')

        # 直接把self.user放到self.request中 ==> request中包含用户的登录信息
        self.request.user = self.user


class TestQuestionListView(BaseQATest):
    """测试问题列表"""

    def test_context_data(self):
        """测试返回的上下文"""
        # 将request请求，传递给 views.QuestionListView
        response = self.get(views.QuestionListView, request=self.request)

        # 判断状态码是不是为200
        self.assertEqual(response.status_code, 200)

        # 查询集是否相等
        self.assertQuerysetEqual(
            response.context_data['questions'],  # 查询集的结果
            map(repr, [self.question_one, self.question_two]),  # TODO： 高阶函数：map [repr(self.question_one), repr(self.question_two)]
            ordered=False  # 是否按照顺序对比
        )

        # TODO：再使用高级一点的函数 ： zip(), all()
        # self.assertTrue(all(a == b for a, b in zip(response.context_data['questions'], Question.objects.all())))

        # 直接判断上下文的断言方法
        self.assertContext('popular_tags', Question.objects.get_counted_tags())
        self.assertContext('active', 'all')


class TestAnsweredQuestionListView(BaseQATest):
    """测试已回答问题列表"""

    def test_context_data(self):
        response = self.get(views.AnsweredQuestionListView, request=self.request)  # 方式一
        # response = views.AnsweredQuestionListView.as_view()(self.request)  # 方式二

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data['questions'], [repr(self.question_two)])
        self.assertContext('active', 'answered')  # 对应方式一
        # self.assertEqual(response.context_data['active'], 'answered')  # 对应方式二


class TestUnansweredQuestionListView(BaseQATest):
    """测试未回答问题列表"""

    def test_context_data(self):
        response = self.get(views.UnansweredQuestionListView, request=self.request)  # 方式一
        self.assertEqual(response.status_code, 200)  # TODO：或者 self.response_200(response)
        self.assertQuerysetEqual(response.context_data['questions'], [repr(self.question_one)])
        self.assertContext('active', 'unanswered')


class TestCreateQuestionView(BaseQATest):
    """
    测试创建问题
    TODO: 通用类视图中的单元测试，测的是数据的结果，而不是数据在视图中的流转过程
    """

    def test_get(self):
        response = self.get(views.CreateQuestionView, request=self.request)
        self.response_200(response)

        # assertContains() 是否包含的意思
        self.assertContains(response, '标题')
        # self.assertContains(response, '编辑')
        # self.assertContains(response, '预览')
        self.assertContains(response, '标签')

        # 这里Django源码中，对上下文的封装
        self.assertIsInstance(response.context_data['view'], views.CreateQuestionView)

    def test_post(self):
        data = {'title': 'title', 'content': 'content', 'tags': 'tag1,tag2', 'status': 'O'}

        # 这里的URL可以随便写，因为不经过Django的路由
        # 但是data中的参数不能乱写，因为都是需要校验的数据
        request = RequestFactory().post('/fake-url', data=data)
        request.user = self.user

        # RequestFactory测试含有django.contrib.messages的视图 https://code.djangoproject.com/ticket/17971
        # 这里有个django的中间件，但是由于是基于RequestFactory()做的单元测试
        # 这里是不走django的中间件的，就需要使用FallbackStorage()处理这个异常
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = self.post(views.CreateQuestionView, request=request)
        # 用户提交问题之后，跳转到unanswered的页面
        assert response.status_code == 302
        assert response.url == '/qa/unanswered/'


class TestQuestionDetailView(BaseQATest):
    """测试问题详情"""

    def get_context_data(self):
        # 这里的pk，是url中的请求参数
        response = self.get(views.QuestionDetailView, request=self.request, pk=self.question_one.id)
        self.response_200(response)
        self.assertEqual(response.context_data['question'], self.question_one)


class TestCreateAnswerView(BaseQATest):
    """测试创建回答"""

    def test_get(self):
        response = self.get(views.CreateAnswerView, request=self.request, question_id=self.question_one.id)
        self.response_200(response)

        # 查看返回的页面中是否包含“编辑”、“预览”
        # self.assertContains(response, '编辑')
        # self.assertContains(response, '预览')

        # 查看response中的context_data中的view，是不是views.CreateAnswerView中的实例化对象
        self.assertIsInstance(response.context_data['view'], views.CreateAnswerView)

    def get_post(self):
        request = RequestFactory().post('/fake-url', data={'content': 'content'})
        request.user = self.user

        # RequestFactory测试含有django.contrib.messages的视图 https://code.djangoproject.com/ticket/17971
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = self.post(views.CreateAnswerView, request=request)
        assert response.status_code == 302

        # TODO：新的传值方式，效率更高（python3.6之后的版本中才有）
        assert response.url == f'/qa/question-detail/{self.question_one.id}'


class TestQAVote(BaseQATest):
    """给问题、回答投票"""

    def setUp(self):
        super(TestQAVote, self).setUp()

        # HTTP_X_REQUESTED_WITH='XMLHttpRequest'：把这个请求变成Ajax请求
        self.request = RequestFactory().post('/fake-url', HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # QueryDict instance is immutable, request.POST是QueryDict对象，不可变
        self.request.POST = self.request.POST.copy()

        self.request.user = self.other_user

    def test_question_upvote(self):
        """赞同问题"""
        self.request.POST['question'] = self.question_one.id
        self.request.POST['value'] = 'U'

        response = views.question_vote(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['votes'] == 1

    def test_question_downvote(self):
        """反对问题"""
        self.request.POST['question'] = self.question_two.id
        self.request.POST['value'] = 'D'

        response = views.question_vote(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['votes'] == -1

    def test_answer_upvote(self):
        """赞同问答"""
        self.request.POST['answer'] = self.answer.uuid_id
        self.request.POST['value'] = 'U'

        response = views.answer_vote(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['votes'] == 1

    def test_answer_downvote(self):
        """反对回答"""
        self.request.POST['answer'] = self.answer.uuid_id
        self.request.POST['value'] = 'D'

        response = views.answer_vote(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['votes'] == -1

    def test_accept_answer(self):
        """接受回答"""

        self.request.user = self.user  # self.user是提问者
        self.request.POST['answer'] = self.answer.uuid_id

        response = views.accept_answer(self.request)

        assert response.status_code == 200
        assert json.loads(response.content)['status'] == 'true'


"""
使用TestClient和RequestFactory测试视图的区别：
    RequestFactory: 生成WSGIRequest供使用，与Django代码无关，单元测试的最佳实践，但使用难度高
    TestClient: 走Django框架的整个请求响应流程，经过WSGI handler、中间件、URL路由、上下文处理器，返回response，更像是集成测试。
        特点：使用简单，测试一步到位。
             测试用例运行慢，依赖于中间件、URL路由等其它部分
"""
