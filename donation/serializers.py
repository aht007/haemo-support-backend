from rest_framework import serializers
from .models import DonationRequest

class DonationSerializer(serializers.ModelSerializer):
     class Meta:
        model = DonationRequest
        fields = '__all__'
