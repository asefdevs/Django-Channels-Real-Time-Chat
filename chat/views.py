from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import Room, Message
from django.db.models import Q

from auth_chat.models import (
    CustomUser,
    Contacts,
) 
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from chat.serializers import (
    AddContactSerializer,
    MyContactsSerializer,
    StartChatRoomSerializer,
    ChatRoomRetrieveSerializer,
)

class AddContactAPIView(generics.CreateAPIView):
    queryset = Contacts.objects.all()
    serializer_class = AddContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeleteContactAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, contact_id):
        try:
            contact = Contacts.objects.get(user = self.request.user, contacts=contact_id)
            contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contacts.DoesNotExist:
            return Response({"message": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)

 
class MyContactsAPIView(generics.ListAPIView):
    queryset = Contacts.objects.all()
    serializer_class = MyContactsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contacts.objects.filter(user=self.request.user)
    
class StartChatRoomAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StartChatRoomSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            second_user = serializer.validated_data.get('second_user')
            existing_room = Room.objects.filter(
                Q(first_user=request.user, second_user=second_user) | Q(first_user=second_user, second_user=request.user)
            ).first()
            if not existing_room:
                serializer.save(first_user=self.request.user)
                existing_room = serializer.instance  

            response_data = {"room_id": existing_room.id}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChatRoomRetrieveView(generics.RetrieveAPIView):
    serializer_class = ChatRoomRetrieveSerializer
    queryset = Room.objects.all()

    def get(self, request, room_id):
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response({'message': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(room)
        return Response(serializer.data)

# def index(request):
#     users = CustomUser.objects.all().exclude(id=request.user.id)

#     return render(request, "chat/index.html", {"users": users})

# def room(request, room_name):
#     users = CustomUser.objects.all().exclude(id=request.user.id)
#     messages = Message.objects.filter(room_id=room_name)
#     try:
#         room = Room.objects.get(id=room_name)
#     except:
#         return HttpResponse("Room not found")
#     context = {
#         "room_name": room_name,
#         "users": users,
#         "messages": messages,
#         "room": room,
#     }
#     return render(request, "chat/room_v2.html", context)




# def start_chat(request, username):
#     second_user = CustomUser.objects.get(username=username)
#     try:
#         room = Room.objects.get(first_user=request.user, second_user=second_user)
#     except:
#         try :
#             room = Room.objects.get(first_user=second_user, second_user=request.user)
#         except:
#             room = Room.objects.create(first_user=request.user, second_user=second_user)
#     return redirect('room', room_name=room.id)

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)  
#             return redirect('index')

#     return render(request, "chat/login.html")
