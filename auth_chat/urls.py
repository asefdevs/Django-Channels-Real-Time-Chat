from django.urls import path
from auth_chat.views import (
    UserRegisterAPIView,
    GenerateOTPAPIView,
    VerifyOTPAPIView,
    AllUsers,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('register/',UserRegisterAPIView.as_view(), name='register'),
    path('generate-otp/', GenerateOTPAPIView.as_view(), name='generate-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),

    path('all-users/', AllUsers.as_view(), name='all-users'),
    
]
