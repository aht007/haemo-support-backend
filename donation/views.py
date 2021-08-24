from django.core.exceptions import ValidationError
from donation.serializers import DonationSerializer
from donation.models import DonationRequest
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status


class DonationView(APIView):
    def get(self, request):
        # get last 50 latest requests
        if(request.user.is_admin):
            data = reversed(DonationRequest.objects
                            .filter(Q(is_approved=False))
                            .order_by('-time')[:50]
                            )
        else:
            data = reversed(DonationRequest.objects.filter(
                Q(is_approved=True)
            ).order_by('-time')[:50]
            )
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

    def validate_ids(self, id_list):
        for id in id_list:
            try:
                DonationRequest.objects.get(id=id)
            except (DonationRequest.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def put(self, request, *args, **kwargs):
        id_list = request.data['ids']
        self.validate_ids(id_list=id_list)
        instances = []
        for id in id_list:
            obj = self.get_object(pk=id)
            obj.is_approved = True
            obj.save()
            instances.append(obj)
        serializer = DonationSerializer(instances, many=True)
        return Response(serializer.data)


class UserRequestsView(generics.ListCreateAPIView):
    def get_queryset(self):
        return DonationRequest.objects.filter(created_by=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DonationSerializer(queryset, many=True)
        return Response(serializer.data)


class DonationDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DonationRequest.objects.all()
    serializer_class = DonationSerializer
