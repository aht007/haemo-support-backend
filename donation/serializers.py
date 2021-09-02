from rest_framework import serializers
from .models import DonationRequest


class DonationUserActionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DonationRequest
        fields = ['id', 'blood_group', 'quantity',
                  'location', 'priority', 'description',
                  'document']

    def switch(self, bloodGroup):
        """
        Switch Statement for getting blood group to slug mapping
        """
        switcher = {
            "A+": "a_positive",
            "B+": "b_positive",
            "AB+": "ab_positive",
            "O+": "o_positive",
            "A-": "a_negative",
            "B-": "b_negative",
            "AB-": "ab_negative",
            "O-": "o_negative",
        }
        return switcher.get(bloodGroup)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        donation_request = DonationRequest.objects.create(
            **validated_data,
            search_slug=self.switch(validated_data['blood_group'])
        )
        return donation_request


class DonationGetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='created_by.username', default='')

    class Meta:
        model = DonationRequest
        fields = ['id', 'blood_group', 'quantity',
                  'location', 'priority', 'is_approved',
                  'is_rejected', 'is_complete', 'description',
                  'document', 'username', 'in_progress', 'comments']


class DonationAdminActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = ['id', 'is_approved', 'is_rejected', 'comments']


class DonationInProgressActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = ['id', 'in_progress']
