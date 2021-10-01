"""
Views for Accounts App
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import (authentication_classes,
                                       permission_classes)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from accounts.models import User
from .serializers import (BaseSerializer, MyTokenObtainPairSerializer,
                          UserSerializer, RegisterSerializer, LoginSerializer)
from .services import send_mail_to_new_users


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
    serializer_class = BaseSerializer

    def send_password_creation_mail_to_users(self, request, users):
        """
        Utility function to send mail to users
        """
        domain = get_current_site(request)
        send_mail_to_new_users(users, domain)

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
class SetPasswordView(APIView):
    """
    View for checking the token validity and setting new password functionality
    """

    def get_user(self, uidb64):
        """
        function to return user from given base 64 encoded user id
        """
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        return user

    def check_token_validity(self, user, token):
        """
        function to check given token's validity... returns boolean as result
        """
        token_generator = PasswordResetTokenGenerator()
        return token_generator.check_token(user, token)

    def get(self, request):
        """
        Method for checkiung token validity
        """
        try:
            user = self.get_user(request.GET.get('uidb64'))
            is_token_valid = self.check_token_validity(
                user, request.GET.get('token'))
            if(user is not None and is_token_valid):
                return Response({
                    "data": "Token is valid and not expired"
                })
            else:
                return Response({
                    "data": "Token is invalid"},
                    status=status.HTTP_403_FORBIDDEN)

        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist) as exc:
            return Response({"error": str(exc)},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        Post method for validating uid and token and
        then creating password for user
        """
        try:
            uidb64 = request.data.get('uidb64')
            token = request.data.get('token')
            user = self.get_user(uidb64)
            is_token_valid = self.check_token_validity(
                user, token)
            if(user is not None and is_token_valid):
                user.set_password(request.data.get('password'))
                user.save()
                return Response({
                    "data": "Password Changed Successfully"
                })
            else:
                return Response({
                    "data": "Token is invalid"},
                    status=status.HTTP_403_FORBIDDEN)

        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist) as exc:
            return Response({"error": str(exc)},
                            status=status.HTTP_400_BAD_REQUEST)
