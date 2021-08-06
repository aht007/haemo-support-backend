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
        fields = ['id','name', 'date_occured','date_cured']

    def create(self, validated_data):
        illness = Illness.objects.create(
            **validated_data,
            medical_profile_id = self.context['request'].user.health_profile
        )
        return illness