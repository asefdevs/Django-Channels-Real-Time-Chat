from django.db import models
from django.contrib.auth.models import User
import uuid


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ChatUser(models.Model):
    user = models.ForeignKey(User, related_name= 'chat_user' , on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name= 'chat_users' , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    room = models.ForeignKey(Room, related_name= 'messages' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= 'messages' , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self): 
        return self.content