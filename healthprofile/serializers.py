"""
Serializers for Health Profile App
"""

from rest_framework import serializers
from .models import HealthProfile, Illness


class HealthProfileSerializer(serializers.ModelSerializer):
    """
    Health Profile Model Serializer
    """
    class Meta:
        model = HealthProfile
        fields = ['id', 'times_donated']

    def create(self, validated_data):
        """
        Overriding created method to attach user
        """
        healthProfile = HealthProfile.objects.create(
            **validated_data,
            user_id=self.context['request'].user
        )
        return healthProfile


class IllnessSerializer(serializers.ModelSerializer):
    """
    Illness Model Serializer
    """
    class Meta:
        model = Illness
        fields = ['id', 'name', 'date_occured', 'date_cured']

    def create(self, validated_data):
        """
        Overriding created method to attach health profile
        """
        illness = Illness.objects.create(
            **validated_data,
            medical_profile_id=self.context['request'].user.health_profile
        )
        return illness
