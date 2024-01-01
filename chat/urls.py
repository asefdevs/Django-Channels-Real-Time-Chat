from django.urls import path

from . import views
from chat.views import (
    AddContactAPIView,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("auth/login/", views.login_view, name="login"),
    path('room/<str:username>/', views.start_chat, name='start_chat'),

    path('api/add-contact/', AddContactAPIView.as_view(), name='add-contact'),




]