from rest_framework import serializers
from .models import DonationRequest

class DonationSerializer(serializers.ModelSerializer):
   class Meta:
      model = DonationRequest
      fields = ['id', 'blood_group', 'quantity', 'location', 'priority', 'is_approved']
        
   def create(self, validated_data):
      donation_request = DonationRequest.objects.create(
            **validated_data,
            created_by = self.context['request'].user
            )
      return donation_request


