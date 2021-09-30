"""
Views for Accounts App
"""

from rest_framework import generics, permissions
from rest_framework.response import Response

from rest_framework.decorators import (authentication_classes,
                                       permission_classes)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from accounts.models import User
from accounts.services import MailService
from .serializers import (BulkRegisterSerializer, MyTokenObtainPairSerializer,
                          UserSerializer, RegisterSerializer, LoginSerializer)


@authentication_classes([])
@permission_classes([])
class UserRegisterView(generics.GenericAPIView):
    """
    View for User Registration
    """

    def post(self, request):
        """
        Post Action handler
        """
        serialaizer = RegisterSerializer(data=request.data)
        serialaizer.is_valid(raise_exception=True)
        user = serialaizer.save()
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data
        })


class IsUserAuthorized(permissions.BasePermission):
    """
    Get User Permission for object
    """

    def has_object_permission(self, request, view, user_obj):

        permission = user_obj.id == request.user.id or request.user.is_admin
        return permission


class UserEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for Editing user
    """
    permission_classes = [
        IsUserAuthorized,
    ]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(generics.GenericAPIView):
    """
    View for User Login
    """
    @authentication_classes([])
    @permission_classes([])
    def post(self, request):
        """
        Post Action Handler
        """
        serialaizer = LoginSerializer(data=request.data)
        serialaizer.is_valid(raise_exception=True)
        user = serialaizer.validated_data
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data
        })

    def get(self):
        """
        Get All users or return user data for current user
        """
        user = self.request.user
        if user.is_superuser:
            queryset = User.objects.all().order_by('-date_joined')
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            user = User.objects.filter(username=user.username)
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)


class UserAPI(generics.RetrieveAPIView):
    """
    Get User's Own data
    """
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MyTokenObtainPairView(TokenObtainPairView):
    """
    View for getting JWT Token
    """
    serializer_class = MyTokenObtainPairSerializer


@permission_classes([permissions.IsAdminUser])
class BulkUserCreationView(generics.GenericAPIView):
    """
    View for Bulk User Registration
    """
    serializer_class = BulkRegisterSerializer

    def send_password_creation_mail_to_users(self, request, users):
        """
        Utility function to send mail to userX
        """
        for user in users:
            MailService.send_email_for_password_creation(request, user)

    def post(self, request):
        """
        Post action for bulk user creation
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        users = serializer.save()
        self.send_password_creation_mail_to_users(request, users)
        return Response(
            serializer.data
        )


@permission_classes([])
@authentication_classes([])
class SetPasswordView(generics.GenericAPIView):
    """
    View for checking the token validity and setting new password functionality
    """

    def get(self, request, uidb64, token):
        """
        Method for checkiung token validity
        """
        return Response({})
