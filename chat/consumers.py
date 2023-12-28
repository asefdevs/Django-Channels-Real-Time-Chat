import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message, Room

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
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