from rest_framework import serializers
from .models import DonationRequest

class DonationSerializer(serializers.ModelSerializer):
   class Meta:
      model = DonationRequest
      fields = ['id', 'blood_group', 'quantity', 'location']
        
   def create(self, validated_data):
      donation_request = DonationRequest.objects.create(
            **validated_data
            )
      return donation_request