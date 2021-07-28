from django.urls import path, include
from .views import RegisterAPI, LoginAPI, UserAPI,UsersList

urlpatterns = [
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/user', UserAPI.as_view()),
    path('auth/users', UsersList.as_view()),
]