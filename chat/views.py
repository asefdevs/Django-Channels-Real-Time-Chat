from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import Room, Message

def index(request):
    users = User.objects.all().exclude(id=request.user.id)

    return render(request, "chat/index.html", {"users": users})

def room(request, room_name):
    users = User.objects.all().exclude(id=request.user.id)
    messages = Message.objects.filter(room_id=room_name)
    try:
        room = Room.objects.get(id=room_name)
    except:
        return HttpResponse("Room not found")
    context = {
        "room_name": room_name,
        "users": users,
        "messages": messages,
        "room": room
    }
    return render(request, "chat/room_v2.html", context)


def start_chat(request, username):
    second_user = User.objects.get(username=username)
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
