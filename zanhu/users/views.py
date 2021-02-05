from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

User = get_user_model()


# LoginRequiredMixin: 指定必须用户登录之后才可以访问到
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        """用户个人信息数据统计"""
        content = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)

        # TODO: 这里全部使用 外间的反向查询
        content["moments_num"] = user.publisher.filter(reply=False).count()
        content["article_num"] = user.author.filter(status="P").count()

        # from django_comments.models import Comment ==> 这里要查看源码中的comment中的外键字段
        content["comment_num"] = user.publisher.filter(reply=True).count() + user.comment_comments.all().count()
        content["question_num"] = user.q_author.all().count()
        content["answer_num"] = user.a_author.all().count()

        # 互动数 = 动态点赞数 + 问答点赞数 + 评论数 + 私信用户数(双方都有发送和接受私信)
        tmp = set()
        # 我发送私信给多少不同的用户：
        send_num = user.sent_messages.all()
        for s in send_num:
            tmp.add(s.recipient.username)
        # 我接受的私信来自多少不同的用户：
        received_num = user.received_messages.all()
        for r in received_num:
            tmp.add(r.sender.username)

        content["interaction_num"] = user.liked_news.all().count() + user.qa_vote.all().count() + content["comment_num"] + len(tmp)

        return content


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """用户只能更新自己的信息"""
    model = User
    template_name = "users/user_form.html"
    fields = [  # 允许用户进行更改的字段
        "nickname",
        "job_title",
        "introduction",
        "picture",
        "location",
        "personal_url",
        "weibo",
        "zhihu",
        "github",
        "linkedin"
    ]

    def get_success_url(self):
        """更新成功之后跳转的页面(用户自己的页面)"""
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):
        # return User.objects.get(username=self.request.user.username)
        return self.request.user
