import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message, Room
from rest_framework_simplejwt.tokens import AccessToken
from auth_chat.models import CustomUser
from rest_framework_simplejwt.exceptions import TokenError


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        token = self.scope["url_route"]["kwargs"]["token"]
        try:
            access_token_obj = AccessToken(token)
            user_id = access_token_obj['user_id']
            self.user = CustomUser.objects.get(id=user_id)
        except TokenError: 
            self.disconnect(404)
            return
        except CustomUser.DoesNotExist:
            self.disconnect(404)
            return
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.user
        message_content = Message.objects.create(user=user, content=message, room_id = self.room_name)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat.message",
                "message": message,
                "user": user.username,
                'created_at': message_content.created_at.strftime('%H:%M')
            }
        )

    def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        created_at = event['created_at']
        self.send(text_data=json.dumps(
            {
                "message": message,
                "user": user,
                'created_at': created_at
            }
            ))