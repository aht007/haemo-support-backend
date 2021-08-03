from accounts.serializers import UserSerializer
from rest_framework import serializers
from .models import HealthProfile, Illness
from django.contrib.auth import authenticate

class HealthProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthProfile
        fields = ['id', 'times_donated']

    def create(self, validated_data):
        healthProfile = HealthProfile.objects.create(
            **validated_data,
            user_id = self.context['request'].user
        )
        return healthProfile

class IllnessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Illness
        fields = "__all__"