from rest_framework.response import Response

from auth_chat.models import CustomUser
from auth_chat.permissions import IsAdmin

from auth_chat.serializers import (
    UserCreateSerializer,
    GenerateOTPSerializer,
    VerifyOTPSerializer,
    AllUsersSerializer,
    UserProfileRetrieveSerializer,
    UserProfileUpdateSerializer,
)
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework import status
from .utils.otp_generator import generate_otp, generate_secret_key, verify_otp

from rest_framework_simplejwt.tokens import AccessToken

class AllUsers(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AllUsersSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        user = self.request.user
        acces_token = AccessToken.for_user(user)
        
        print(acces_token)
        return super().get_queryset().exclude(id=self.request.user.id)

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class GenerateOTPAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GenerateOTPSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            secret_key = generate_secret_key()
            otp = generate_otp(secret_key)
            response_data = {
                'secret_key': secret_key,
                'otp': otp,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
    
class VerifyOTPAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            user = CustomUser.objects.filter(phone=phone_number).first()
            user.is_active = True
            user.save()
            return Response({'message': 'Verified Succesfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)