from auth_chat.models import CustomUser
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username','email', 'password', 'password2', 'phone', 'address']


    def validate(self,data):
        password = data['password']
        password2 = data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if len(password) < 3:
            raise serializers.ValidationError({'password': 'Password must be at least 8 characters.'})
        
        existing_email = CustomUser.objects.filter(email=data['email']).first()
        if existing_email:
            raise serializers.ValidationError({'email': 'Email already exists.'})
        
        existing_username = CustomUser.objects.filter(username=data['username']).first()
        if existing_username:
            raise serializers.ValidationError({'username': 'Username already exists.'})
        
        existing_number = CustomUser.objects.filter(phone=data['phone']).first()
        if existing_number:
            raise serializers.ValidationError({'phone': 'Phone number already exists.'})
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user