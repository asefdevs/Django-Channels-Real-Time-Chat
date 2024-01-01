from auth_chat.models import CustomUser
from rest_framework import serializers
from auth_chat.utils.otp_generator import generate_otp, generate_secret_key, verify_otp
class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'password2', 'phone', 'address']


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
    
class GenerateOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)

    def validate(self, data):
        phone = data['phone']
        user = CustomUser.objects.filter(phone=phone).first()
        if not user:
            raise serializers.ValidationError({'phone': 'User does not exist.'})
        if user.is_active:
            raise serializers.ValidationError({'phone': 'User is already active.'})
        return data
    
class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=100)
    otp = serializers.CharField(max_length=100)
    secret_key = serializers.CharField(max_length=100)

    def validate(self, data):
        phone_number = data['phone_number']
        otp = data['otp']
        secret_key = data['secret_key']
        user = CustomUser.objects.filter(phone=phone_number).first()
        if not user:
            raise serializers.ValidationError({'phone_number': 'User does not exist.'})
        if user.is_active:
            raise serializers.ValidationError({'phone_number': 'User is already active.'})
        if not verify_otp(secret_key,otp):
            raise serializers.ValidationError({'otp': 'OTP is incorrect.'})
        return data
    
class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']