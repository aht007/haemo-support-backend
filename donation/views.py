from donation.serializers import DonationSerializer
from donation.models import DonationRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class DonationView(APIView):
    def get(self, request):
    # get last 50 latest requests  
        data = reversed(DonationRequest.objects.order_by('-time')[:50])
        donation_requests = DonationSerializer(data, context=request,many=True).data
        return Response(
            donation_requests
        )
        