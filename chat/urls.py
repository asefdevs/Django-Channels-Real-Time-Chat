from django.urls import path

from . import views
from chat.views import (
    AddContactAPIView,
    MyContactsAPIView,
    StartChatRoomAPIView,
    DeleteContactAPIView,
    ChatRoomRetrieveView,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("auth/login/", views.login_view, name="login"),
    path('room/<str:username>/', views.start_chat, name='start_chat'),

    path('api/add-contact/', AddContactAPIView.as_view(), name='add-contact'),
    path('api/delete-contact/<int:contact_id>/', DeleteContactAPIView.as_view(), name='delete-contact'),
    path('api/my-contacts/', MyContactsAPIView.as_view(), name='my-contacts'),

    path('api/start-chat-room/', StartChatRoomAPIView.as_view(), name='start-chat-room'),




]