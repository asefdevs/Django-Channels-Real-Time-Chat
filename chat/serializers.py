from rest_framework import serializers
from auth_chat.models import (
    CustomUser, 
    Contacts, 
    )
from chat.models import (
    Room,
    Message,
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
        if not CustomUser.objects.filter(id=contacts.id,is_active =True).exists():
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


class StartChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['second_user']

    def validate_second_user(self,value):
        user = self.context['request'].user
        contact_exist = Contacts.objects.filter(user=user, contacts=value).first()
        if not contact_exist:
            raise serializers.ValidationError({'second_user': 'User not in your contacts.'})
        return value
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','user','content','created_at']
    
class ChatRoomRetrieveSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    class Meta:
        model = Room
        fields = ['id','name','messages']

    def validate(self, data):
        user = self.context['request'].user
        room = self.instance
        if room.first_user != user or room.second_user != user:
            raise serializers.ValidationError({'name': 'You are not allowed to access this room.'})
        return data
