from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from zanhu.news.views import NewsListView

urlpatterns = [
                  # 站点管理
                  # path(settings.ADMIN_URL, admin.site.urls),

                  # 配置首页
                  path("", NewsListView.as_view(), name="home"),

                  # 用户管理
                  path("users/", include("users.urls", namespace="users")),

                  # 开发的应用
                  path("news/", include("news.urls", namespace="news")),
                  path("articles/", include("articles.urls", namespace="articles")),
                  path("qa/", include("qa.urls", namespace="qa")),
                  path('messages/', include('messager.urls', namespace='messages')),
                  path('notifications/', include('notifications.urls', namespace='notifications')),

                  # 第三方应用
                  path('markdownx/', include('markdownx.urls')),
                  path('comments/', include('django_comments.urls')),
                  path('search/', include('haystack.urls')),

                  path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
                  # path("users/", include("zanhu.users.urls", namespace="users")),
                  path("accounts/", include("allauth.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("api/", include("config.api_router")),
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path(
            "500/",
            default_views.server_error
        ),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
