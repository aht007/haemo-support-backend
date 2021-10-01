"""
Serializer class for Accounts App
"""
import datetime

from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import User


class BaseSerializer(serializers.ModelSerializer):
    """
    Base User Serializer
    """
    class Meta:
        """
        Initializing the serializer with proper data
        """
        model = User
        fields = ['id', 'username', 'email', 'date_of_birth',
                  'phone_number', 'blood_group']

    def create(self, validated_data):
        """
        Overriding the create method to attach custom fields
        """
        password = User.objects.make_random_password()
        user = User.objects.create_user(
            **validated_data,
            password=password
        )
        return user


class UserSerializer(BaseSerializer):
    """
    Serializer for getting Complete User Data at frotnend
    """
    class Meta:
        """
        Initializing the serializer with proper data
        """
        model = User
        fields = BaseSerializer.Meta.fields+['is_admin']


class RegisterSerializer(BaseSerializer):
    """
    Serailizer for registering an account
    """
    class Meta:
        """
        Initializing the serializer with proper data
        """
        model = User
        fields = BaseSerializer.Meta.fields+['is_admin', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Overriding the create method to attach custom fields
        """
        user = User.objects.create_user(
            **validated_data,
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for Performing Login
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate the user data for login
        """
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Token obatain serializer class override for custom claims
    """
    @classmethod
    def get_token(cls, user):
        """
        Adding custom claims
        """
        token = super().get_token(user)

        # Add custom claims
        token['iat'] = token.current_time
        token['user'] = user.username
        token['date'] = str(datetime.date.today())
        return token
