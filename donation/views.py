from donation.serializers import DonationSerializer
from donation.models import DonationRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

class DonationView(APIView):
    def get(self, request):
        # get last 50 latest requests
        data = reversed(DonationRequest.objects.filter( Q(created_by=request.user) | Q(is_approved=True) ).order_by('-time')[:50])
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

class ModifyDonationStatusView(APIView):
    def get_object(self, pk):
        return DonationRequest.objects.get(id=pk)

    def post(self, request, pk):
        object = self.get_object(pk)
        serializer = DonationSerializer(
            object, data=request.data, partial=True)
        if serializer.is_valid():
            donation = serializer.save()
            profile = DonationSerializer(donation, context=request).data
            return Response(
                profile
            )
        return Response(
            code=400, data='Wrong Parameters'
        )