from accounts.serializers import UserSerializer
from rest_framework import serializers
from .models import HealthProfile, Illness
from django.contrib.auth import authenticate

class HealthProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = HealthProfile
        fields = "__all__"

    def create(self, validated_data):
        healthProfile = HealthProfile.objects.create(
            **validated_data,
            user_id = self.context['request'].user.id
        )
        return healthProfile

class IllnessSerializer(serializers.ModelSerializer):
    healthProfile = HealthProfileSerializer(read_only=True)

    class Meta:
        model = Illness
        fields = "__all__"