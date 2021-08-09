from accounts.serializers import RegisterSerializer
from django.urls import path
from .views import  MyTokenObtainPairView, UserLoginView, UserRegisterView, UserAPI
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('auth/register', UserRegisterView.as_view()),
    path('auth/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user', UserAPI.as_view()),
    path('auth/users', UserLoginView.as_view()),
    path('auth/user/edit', UserRegisterView.as_view(), name="edit_user")
]