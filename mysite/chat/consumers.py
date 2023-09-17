import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "rooms_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Add the user to the room
        await self.add_user_to_room()

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Remove the user from the room
        await self.remove_user_from_room()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room = text_data_json["room"]

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                'username': username,
                'room': room
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room = event["room"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "room": room,
        }))

        # Send user online event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_online",
                "online_users": get_online_users_in_room(self.room_group_name),
            },
        )

    async def user_online(self, event):
        # Обновление списка онлайн пользователей

        # Получение списка онлайн пользователей из события
        online_users = event['online_users']

        # Отправка обновленного списка в клиент
        await self.send(text_data=json.dumps({
            'online_users': online_users
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)

    @sync_to_async
    def add_user_to_room(self):
        user = User.objects.get(username=self.scope["user"].username)
        room = Room.objects.get(slug=self.room_name)
        room.users.add(user)

    @sync_to_async
    def remove_user_from_room(self):
        user = User.objects.get(username=self.scope["user"].username)
        room = Room.objects.get(slug=self.room_name)
        room.users.remove(user)

    @sync_to_async
    def get_online_users_in_room(room_group_name):
        group_info = ChannelLayerWrapper.get_channel_layer().group_channels(room_group_name)
        # Extract online users from the group info and return the list
        return [user.split('_')[-1] for user in group_info]
