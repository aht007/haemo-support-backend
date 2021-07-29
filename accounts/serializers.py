from rest_framework import serializers
from .models import my_user
from django.contrib.auth import authenticate

# USER Serilaizer....


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_user
        fields = ('id', 'username', 'email', 'date_of_birth',
                  'phone_number', 'blood_group')

# Register


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_user
        fields = ('id', 'username', 'email', 'date_of_birth',
                  'password', 'phone_number', 'blood_group')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = my_user.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'], validated_data['date_of_birth'], validated_data['phone_number'], validated_data['blood_group'])
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
