from channels.generic.websocket import AsyncWebsocketConsumer
import json


class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f"user_{self.room_name}"

        print("room group name", self.room_group_name)
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect", close_code)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        pass

    
    async def task_assign(self, event):
        print("task assign", event)
        await self.send(text_data=json.dumps({
            'task_id': event['task_id'],
            'image_url': event['image_url'],
            'details': event['details'],
            'options': event['options']
        }))




# channel_layer.group_send(
# "user_3",
# {
#     "type": "task_assign",
#     **event
# })