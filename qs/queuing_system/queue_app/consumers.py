import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QueueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "queue_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "queue_group",
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            "queue_group",
            {
                'type': 'queue_update',
                'message': text_data
            }
        )

    async def queue_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def ticket_served(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'ticket_served',
            'message': message
        }))
