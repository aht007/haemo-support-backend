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
from .serializers import (MyTokenObtainPairSerializer, UserSerializer,
                          RegisterSerializer, LoginSerializer)


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
