#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MessagesConsumer(AsyncWebsocketConsumer):
    """处理私信应用中WebSocket请求"""

    # 定义方法的地方，前面添加 async
    # 调用方法的地方，前面添加 await
    async def connect(self):
        """WebSocket连接"""
        # 校验用户是否是合法用户
        if self.scope['user'].is_anonymous:  # is_anonymous
            # 未登录的用户拒绝连接
            await self.close()
        else:
            # 加入聊天组，监听频道
            # channel_layer ==> get_channel_layer() ==> ChannelLayerManager() 频道层管理器实例
            # 每两个私信的人建立一个聊天组
            # group_add("第一个参数是组名", "第二个参数是频道的名字")
            # 频道名字，使用默认就可以，return "%s.%s!%s" % (prefix, self.client_prefix, uuid.uuid4().hex,)
            await self.channel_layer.group_add(self.scope['user'].username, self.channel_name)

            # 接受WebSocket连接
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """接收私信"""
        await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        """离开聊天组"""
        # 把当前用户从当前监听的频道组里面移除
        await self.channel_layer.group_discard(self.scope['user'].username, self.channel_name)
