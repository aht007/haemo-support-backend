from django.contrib.auth.models import User
from accounts.models import my_user
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import MyTokenObtainPairSerializer, UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Regsiter Api


@authentication_classes([])
@permission_classes([])
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serialaizer = self.get_serializer(data=request.data)
        serialaizer.is_valid(raise_exception=True)
        user = serialaizer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })
# Login API

class EditUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def patch(self, request):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })


@authentication_classes([])
@permission_classes([])
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serialaizer = self.get_serializer(data=request.data)
        serialaizer.is_valid(raise_exception=True)
        user = serialaizer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })

# it is just a retrieve api and also we need permission like user authenticated and having a tocken
# Get User API

# return logged in user


class UserAPI(generics.RetrieveAPIView):
    # permission_classes = [
    #     permissions.IsAuthenticated,
    # ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# get all users


class UsersList(generics.RetrieveAPIView):

    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # get all users
        user = self.request.user
        if user.is_superuser:
            queryset = my_user.objects.all().order_by('-date_joined')
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            user = my_user.objects.filter(username=user.username)
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer