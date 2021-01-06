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
