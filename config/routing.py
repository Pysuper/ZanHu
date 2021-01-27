# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author   ：zheng xingtao

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from zanhu.messager.consumers import MessagesConsumer

# from zanhu.notifications.consumers import NotificationsConsumer

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
                    # path('ws/notifications/', NotificationsConsumer),
                    path('ws/<str:username>/', MessagesConsumer),
                ])
            )
        )
})
