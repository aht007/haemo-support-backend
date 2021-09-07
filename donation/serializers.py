from rest_framework import serializers
from .models import DonationRequest


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = ['id', 'is_approved', 'is_rejected', 'comments']


class DonationUserSerializer(BaseSerializer):
    username = serializers.CharField(source='created_by.username', default='')

    class Meta:
        read_only_fields = ('is_approved', 'is_rejected',
                            'in_progress', 'comments')
        model = BaseSerializer.Meta.model
        fields = BaseSerializer.Meta.fields+['blood_group', 'quantity',
                                             'location', 'priority',
                                             'is_complete', 'description',
                                             'document', 'username',
                                             'in_progress', 'donated_by',
                                             'created_by']

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

    def update(self, instance, validated_data):
        super(DonationUserSerializer, self).update(
            instance, validated_data)
        if(validated_data.get('is_complete', False) is True):
            instance.in_progress = False
        instance.save()
        return instance


class DonationInProgressActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = ['id', 'in_progress', 'donated_by']

    def update(self, instance, validated_data):
        if(instance.is_approved is True):
            instance.in_progress = validated_data.get(
                'in_progress', instance.in_progress)
            instance.donated_by = self.context['request'].user
        instance.save()
        return instance
