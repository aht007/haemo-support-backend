from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime
# USER Serilaizer....


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_of_birth',
                  'phone_number', 'blood_group', 'is_admin')

# Register


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',
                  'date_of_birth', 'phone_number', 'blood_group', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        blood_group = validated_data.get('blood_group', None)
        is_admin = validated_data.get('is_admin', "0")
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'],
            validated_data['date_of_birth'], validated_data['phone_number'],
            blood_group, validated_data['password'], is_admin
            )
        # validated data is included by django itself
        return user
# Login

# Simply authenticating so not modelSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['iat'] = token.current_time
        token['user'] = user.username
        token['date'] = str(datetime.date.today())
        return token
