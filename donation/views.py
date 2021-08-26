from donation.serializers import DonationSerializer
from donation.models import DonationRequest
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class IsUserAuthorized(permissions.BasePermission):
    def has_object_permission(self, request, view, donation_obj):
        return (donation_obj.created_by.id == request.user.id
                or request.user.is_admin)


class DonationView(APIView):
    def get(self, request):
        # get last 50 latest requests
        if(request.user.is_admin):
            data = reversed(DonationRequest.objects
                            .filter(is_approved=False)
                            .order_by('-time')[:50]
                            )
        else:
            data = reversed(DonationRequest.objects.filter(
                is_approved=True
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


class UserRequestsView(generics.ListCreateAPIView):
    def get_queryset(self):
        return DonationRequest.objects.filter(created_by=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DonationSerializer(queryset, many=True)
        return Response(serializer.data)


class DonationUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsUserAuthorized,
    ]
    queryset = DonationRequest.objects.all()
    serializer_class = DonationSerializer
