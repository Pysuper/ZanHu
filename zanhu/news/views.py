from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from zanhu.news.models import News
from zanhu.utils.helper import ajax_required, AuthorRequiredMixin


# 网站的所有内容要求用户登录后才能看到 ==> LoginRequiredMixin
class NewsListView(LoginRequiredMixin, ListView):
    """首页动态"""
    model = News
    paginate_by = 20  # 分页：url中的?page=
    template_name = "news/news_list.html"  # 默认: '模型类名_list.html'

    def get_queryset(self):
        """
        获取视图的对象列表, 实现动态过滤
        :return: django查询集
        """
        return News.objects.filter(reply=False).select_related('user', 'parent').prefetch_related('liked')

    '''
        def get_ordering(self):
        """
        自定义复杂的排序
        :return:
        """
        pass

    def get_paginate_by(self, queryset):
        """
        处理分页
        :param queryset: 要排序的查询集对象
        :return:
        """
        pass

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        添加额外的上下文
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super().get_context_data()
        context["views"] = 100
        return context
    '''


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = News
    template_name = "news/news_confirm_delete.html"
    success_url = reverse_lazy("news:list")  # 在项目URLConf未加载前使用
    # slug_url_kwarg = "slug"  # 通过url，传入要删除的对象主键ID，默认值是slug
    # pk_url_kwarg = "PK"  # 通过url，传入要删除的对象逐主键ID， 默认值是pk


@login_required  # 要求用户登录
@ajax_required  # 判断当前请求是一个Ajax请求
@require_http_methods(["POST"])  # 指定为POST请求
def post_news(request):
    """发表动态, Ajax POST请求"""
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        # 先把内容渲染到模板中，再把模板发送给前端
        html = render_to_string("news/news_single.html", {"news": posted, "request": request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空！")


@login_required
@ajax_required
@require_http_methods(["POST"])
def like(request):
    """点赞, Ajax POST请求"""
    news_id = request.POST["news"]
    news = News.objects.get(pk=news_id)

    # 取消或者添加赞
    news.switch_like(request.user)

    # 返回点赞的数量
    return JsonResponse({"likes": news.count_likers()})


@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """返回动态的评论，AJAX GET请求"""
    news_id = request.GET['news']
    news = News.objects.select_related('user').get(pk=news_id)  # 不是.get(pk=news_id).select_related('user')
    # render_to_string()表示加载模板，填充数据，返回字符串

    # 没有评论的时候
    news_html = render_to_string("news/news_single.html", {"news": news})

    # 有评论的时候
    thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread()})
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html,
    })


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """评论, Ajax POST请求"""
    post = request.POST["reply"].strip()
    parent_id = request.POST["parent"]
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({"comments": parent.comment_count()})
    else:
        return HttpResponseBadRequest("内容不能为空")


@login_required
@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    """更新互动信息"""
    data_point = request.POST['id_value']
    news = News.objects.get(pk=data_point)
    return JsonResponse({'likes': news.count_likers(), 'comments': news.comment_count()})
