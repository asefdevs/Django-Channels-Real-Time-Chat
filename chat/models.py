from django.db import models
from django.contrib.auth.models import User
import uuid


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    first_user = models.ForeignKey(User, related_name= 'first_user' , on_delete=models.CASCADE, null=True, blank=True)
    second_user = models.ForeignKey(User, related_name= 'second_user' , on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.first_user and self.second_user:
            self.name = f"{self.first_user.username} - {self.second_user.username}"
        super().save(*args, **kwargs)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name= 'messages' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= 'messages' , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self): 
        return self.content