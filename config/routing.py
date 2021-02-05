# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author   ：zheng xingtao

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from zanhu.messager.consumers import MessagesConsumer
from zanhu.notifications.consumers import NotificationsConsumer

application = ProtocolTypeRouter({
    # 'http': # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载
    'websocket':
    # 使用AllowedHostsOriginValidator，允许的访问的源站与settings.py文件中的ALLOWED_HOSTS相同
        AllowedHostsOriginValidator(

            # 认证中间件站(兼容Django认证系统)：AuthMiddlewareStack用于WebSocket认证，集成了CookieMiddleware, SessionMiddleware, AuthMiddleware
            AuthMiddlewareStack(

                # URL路由
                URLRouter([
                    # URL路由匹配
                    path('ws/notifications/', NotificationsConsumer),
                    path('ws/<str:username>/', MessagesConsumer),

                    # TODO: 这里路由的顺序
                    # Django和Consumers的路由是兼容的，也就是说，我们需要处理考虑这里路由请求的顺序
                    # 如果把ws/<str:username>/ 放在上面，notifications就是一个字符串，就直接使用username的路由解析了
                    # 这个情况，github都会存在的
                ])
            )
        )
})
