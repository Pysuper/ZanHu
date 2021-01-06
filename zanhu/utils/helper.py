from functools import wraps
from django.views.generic import View
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied

def ajax_required(func):
    """验证是否是Ajax请求"""

    @wraps(func)  # 不会改变函数名称和函数信息
    def wrap(request, *args, **kwargs):
        # request.is_ajax() # 判断是否为ajax请求
        if not request.is_ajax():
            return HttpResponseBadRequest("不是Ajax请求！")
        return func(request, *args, **kwargs)

    return wrap


class AuthorRequiredMixin(View):
    """验证是否为原作者，用于状态删除、文章编辑"""

    def dispatch(self, request, *args, **kwargs):
        # 状态和文章实例有user属性
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied  # 请求不允许
        return super().dispatch(request, *args, **kwargs)


