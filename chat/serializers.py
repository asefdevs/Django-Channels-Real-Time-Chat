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

    def validate(self, data):
        contacts = data['contacts']
        user = self.context['request'].user
        existing_contact = Contacts.objects.filter(user=user).first()
        if existing_contact:
            for contact in contacts:
                if contact in existing_contact.contacts.all():
                    raise serializers.ValidationError({'contacts': 'Contact already exists.'})
        return data

    
