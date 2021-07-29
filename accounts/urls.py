from django.urls import path, include
from .views import RegisterAPI, LoginAPI, UserAPI,UsersList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user', UserAPI.as_view()),
    path('auth/users', UsersList.as_view()),
]