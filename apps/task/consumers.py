from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        query_string = self.scope["query_string"].decode()
        group_name = None

        # group=notifications_jamshidbek_TaskId
        
        for item in query_string.split("&"):
            if item.startswith("group="):
                group_name = item.split("=", 1)[1]
                break

        if not group_name:
            await self.close()
            return

        self.group_name = group_name
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))
