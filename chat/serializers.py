from rest_framework import serializers
from auth_chat.models import (
    CustomUser, 
    Contacts, 
    ProfilePhoto
    )

class AddContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['contacts']

    
