import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    """处理通知应用中的WebSocket请求"""

    async def connect(self):
        """建立连接"""
        if self.scope["user"].is_anonymous:
            # 未登录用户拒绝连接
            await self.close()
        else:
            # 这里监听的是所有的，指定了组名
            await self.channel_layer.group_add("notifications", self.channel_name)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """将接收到的消息返回给前端"""
        # TODO: 这里接受的是从视图里面发送过来的数据，而不是从前端接受的数据
        await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        """断开连接"""
        await self.channel_layer.group_discard("notifications", self.channel_name)
