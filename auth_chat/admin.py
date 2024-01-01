from django.contrib import admin
from auth_chat.models import CustomUser, Contacts, ProfilePhoto
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Contacts)
admin.site.register(ProfilePhoto)
