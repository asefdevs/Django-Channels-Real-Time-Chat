from django.contrib import admin

from .models import Message, Room, ChatUser

admin.site.register(Message)
admin.site.register(Room)
admin.site.register(ChatUser)

