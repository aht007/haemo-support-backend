"""
URLS for Accounts App
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (BulkUserCreationView, MyTokenObtainPairView, UserLoginView,
                    UserRegisterView, UserAPI, UserEditView, SetPasswordView
                    )


urlpatterns = [
    path('auth/register', UserRegisterView.as_view()),
    path('auth/login', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user', UserAPI.as_view()),
    path('auth/users', UserLoginView.as_view()),
    path('auth/user/<int:pk>/', UserEditView.as_view(), name="edit_user"),
    path('auth/bulk-create-users/',
         BulkUserCreationView.as_view(), name='bulk_create_users'),
    path('auth/set-password/', SetPasswordView.as_view(), name='set-password')
]
