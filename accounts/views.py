from accounts.models import my_user
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import MyTokenObtainPairSerializer, UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


class UserRegisterViews(generics.GenericAPIView):
    # Add a user 
    @authentication_classes([])
    @permission_classes([])
    def post(self, request, *args, **kwargs):
        serialaizer = RegisterSerializer(data=request.data)
        serialaizer.is_valid(raise_exception=True)
        user = serialaizer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })

   # Edit a User
    def patch(self, request):
        user = self.request.user
        serializer = RegisterSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })

    


class UserLoginViews(generics.GenericAPIView):
    
    @authentication_classes([])
    @permission_classes([])
    def post(self, request, *args, **kwargs):
        serialaizer = LoginSerializer(data=request.data)
        serialaizer.is_valid(raise_exception=True)
        user = serialaizer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })


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


class UserAPI(generics.RetrieveAPIView):

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
