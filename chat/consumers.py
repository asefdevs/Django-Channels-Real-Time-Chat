import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message, Room
from rest_framework_simplejwt.tokens import AccessToken
from auth_chat.models import CustomUser


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.token = self.scope['headers']['authorization'].decode('utf-8').split(' ')[1]
        if not self.verify_token(self.token):
            self.close()
        # self.token = self.scope["url_route"]["kwargs"]["token"]
        # access_token_obj = AccessToken(self.token)
        # user_id=access_token_obj['user_id']
        # user=CustomUser.objects.get(id=user_id)
        # if not user:
        #     self.close()
        self.room_group_name = f"chat_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope['user']
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
        
    def verify_token (self, token):
        try:
            access_token_obj = AccessToken(token)
            user_id=access_token_obj['user_id']
            user=CustomUser.objects.get(id=user_id)
            if not user:
                return False
            return True
        except:
            return False