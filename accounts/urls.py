from django.urls import path
from .views import MyTokenObtainPairView, RegisterAPI, LoginAPI, UserAPI,UsersList
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user', UserAPI.as_view()),
    path('auth/users', UsersList.as_view()),
]