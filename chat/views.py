from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import Room, Message
from django.contrib.auth import get_user_model
from auth_chat.models import (
    CustomUser,
    Contacts,
) 
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import generics
from chat.serializers import (
    AddContactSerializer,
)

class AddContactAPIView(generics.CreateAPIView):
    queryset = Contacts.objects.all()
    serializer_class = AddContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        existing_contact = Contacts.objects.filter(user=user).first()
        if existing_contact:
            existing_contact.contacts.add(*serializer.validated_data.get('contacts'))
            existing_contact.save()
        serializer.save(user=self.request.user)


def index(request):
    users = CustomUser.objects.all().exclude(id=request.user.id)

    return render(request, "chat/index.html", {"users": users})

def room(request, room_name):
    users = CustomUser.objects.all().exclude(id=request.user.id)
    messages = Message.objects.filter(room_id=room_name)
    try:
        room = Room.objects.get(id=room_name)
    except:
        return HttpResponse("Room not found")
    context = {
        "room_name": room_name,
        "users": users,
        "messages": messages,
        "room": room,
    }
    return render(request, "chat/room_v2.html", context)

class RommAPI(APIView):
    def get(self, request, room_id):
        messages = Message.objects.filter(room_id=room_id)
        room = Room.objects.get(id=room_id)
        data = {
            'messages': messages,
            'room': room
        }
        return Response(data, status=status.HTTP_200_OK)


def start_chat(request, username):
    second_user = CustomUser.objects.get(username=username)
    try:
        room = Room.objects.get(first_user=request.user, second_user=second_user)
    except:
        try :
            room = Room.objects.get(first_user=second_user, second_user=request.user)
        except:
            room = Room.objects.create(first_user=request.user, second_user=second_user)
    return redirect('room', room_name=room.id)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect('index')

    return render(request, "chat/login.html")
