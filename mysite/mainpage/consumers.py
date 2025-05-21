import json
from channels.generic.websocket import AsyncWebsocketConsumer
from mainpage.models import Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name  # isim zaten chat_x_y

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data['message']
        message = await self.create_message(message_text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'sender': message.sender.username,
                'timestamp': message.timestamp.strftime("%d.%m.%Y %H:%M")
            }
        )

        async def chat_message(self, event):
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'sender': event['sender'],
                'timestamp': event['timestamp'],
            }))

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.get(pk=user_id)

    @database_sync_to_async
    def create_message(self, content):
    return Message.objects.create(
        sender=self.scope["user"],
        receiver=User.objects.get(id=self.scope["url_route"]["kwargs"]["receiver_id"]),
        content=content
    )
