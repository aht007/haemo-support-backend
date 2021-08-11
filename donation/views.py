from donation.serializers import DonationSerializer
from donation.models import DonationRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class DonationView(APIView):
    def get(self, request):
        # get last 50 latest requests
        data = reversed(DonationRequest.objects.order_by('-time')[:50])
        donation_requests = DonationSerializer(
            data, context=request, many=True).data
        return Response(
            donation_requests
        )

    def post(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = DonationSerializer(
            data=request.data, context=context)
        if serializer.is_valid():
            data = serializer.save()
            data = DonationSerializer(data, context=context).data
            return Response(
                data
            )
