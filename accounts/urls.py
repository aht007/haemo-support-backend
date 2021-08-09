from accounts.serializers import RegisterSerializer
from django.urls import path
from .views import  MyTokenObtainPairView, UserRegisterViews, UserLoginViews
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('auth/register', UserRegisterViews.as_view()),
    path('auth/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user', UserLoginViews.as_view()),
    path('auth/users', UserLoginViews.as_view()),
    path('auth/user/edit', UserRegisterViews.as_view(), name="edit_user")
]