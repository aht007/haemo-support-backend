from rest_framework import serializers
from .models import DonationRequest


class DonationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='created_by.username', default='')

    class Meta:
        model = DonationRequest
        fields = ['id', 'blood_group', 'quantity',
                  'location', 'priority', 'is_approved',
                  'is_complete', 'is_rejected', 'description', 'comments',
                  'document', 'username']

    def validate_is_approved(self, value):
        if(value):
            if(self.context['request'].user.is_admin is False):
                raise serializers.ValidationError('This action is not'
                                                  'allowed for Non'
                                                  'Admin Users')
        return value

    def validate_is_rejected(self, value):
        if(value):
            if(self.context['request'].user.is_admin is False):
                raise serializers.ValidationError('This action is not'
                                                  'allowed for Non'
                                                  'Admin Users')
        return value

    def validate_comments(self, value):
        # this field is for admin only....
        # Will add comments if rejecting a donation request
        if(value):
            if(self.context['request'].user.is_admin is False):
                raise serializers.ValidationError('This action is not'
                                                  'allowed for Non'
                                                  'Admin Users')
        return value

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
