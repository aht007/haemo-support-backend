from rest_framework import serializers
from .models import DonationRequest


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = ['id', 'blood_group', 'quantity',
                  'location', 'priority', 'is_approved', 'is_complete']

    def validate_is_approved(self, value):
        if (value):
            if(self.context['request'].user.is_admin is False):
                raise serializers.ValidationError('This action is not'
                                                  'allowed for Non'
                                                  'Admin Users')
        return value

    def create(self, validated_data):
        donation_request = DonationRequest.objects.create(
            **validated_data,
            created_by=self.context['request'].user
        )
        return donation_request
