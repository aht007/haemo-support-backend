"""
Serializer for Donation App
"""
from rest_framework import serializers
from .models import DonationRequest, Status


class BaseSerializer(serializers.ModelSerializer):
    """
    Base Serializer for Donations
    """
    class Meta:
        """
        Initializing the base serializer with appropriate Config
        """
        model = DonationRequest
        fields = ['id', 'comments', 'status']


class DonationUserSerializer(BaseSerializer):
    """
    Serailizer for Users and Admin Actions
    """
    username = serializers.CharField(source='created_by.username', default='')

    class Meta:
        """
        Initializing the serializer with appropriate Config
        """
        model = BaseSerializer.Meta.model
        fields = BaseSerializer.Meta.fields+['blood_group', 'quantity',
                                             'location', 'priority',
                                             'description', 'document',
                                             'username',
                                             ]

    def validate_status(self, value):
        """
        check if status being modified is allowed for current user
        """
        if self.context['request'].user.is_admin is False:
            if value is Status.APPROVED or value is Status.REJECTED:
                raise serializers.ValidationError(
                    "This Action is not Allowed for you")
        return value

    def switch(self, blood_group):
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
        return switcher.get(blood_group)

    def create(self, validated_data):
        """
        Overriding the create method to append serach slug
        """
        validated_data['created_by'] = self.context['request'].user
        donation_request = DonationRequest.objects.create(
            **validated_data,
            search_slug=self.switch(validated_data['blood_group'])
        )
        return donation_request


class BloodDonateActionSerializer(serializers.ModelSerializer):
    """
    Serializer for Donation Action
    """
    class Meta:
        """
        Initializing the serializer with appropriate Config
        """
        model = DonationRequest
        fields = ['id', 'status', 'donor']

    def update(self, instance, validated_data):
        """
        overriding the update method to change status
        to in_progress and attach donor
        """
        if(instance.status == Status.APPROVED):
            instance.status = Status.IN_PROGRESS
            instance.donor = self.context['request'].user
        instance.save()
        return instance
