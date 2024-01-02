from rest_framework import serializers
from auth_chat.models import (
    CustomUser, 
    Contacts, 
    ProfilePhoto
    )

class GetContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','phone','address']

class AddContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['contacts']

    def validate(self, data):
        contacts = data['contacts']
        user = self.context['request'].user
        if not CustomUser.objects.filter(id=contacts.id).exists():
            raise serializers.ValidationError({'contacts': 'User does not exist.'})
        if user == contacts:
            raise serializers.ValidationError({'contacts': 'You can not add yourself.'})
        
        if Contacts.objects.filter(user=user, contacts=contacts).exists():
            raise serializers.ValidationError({'contacts': 'User already in your contacts.'})
        return data


class MyContactsSerializer(serializers.ModelSerializer):
    contacts = GetContactInfoSerializer()
    class Meta:
        model = Contacts
        fields = ['id','contacts']
    
