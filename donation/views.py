"""
Views for Donation App
"""
import datetime
import smtplib
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (generics, permissions, parsers,
                            filters, viewsets, status)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from donation.serializers import (AwaitedDonationSerializer, BaseSerializer,
                                  BloodDonateActionSerializer,
                                  DonationUserSerializer)
from donation.models import DonationRequest, Status
from donation.services import send_awaited_request_notification


class IsUserAuthorized(permissions.BasePermission):
    """
    Check User authorization for accessing object
    """

    def has_object_permission(self, request, view, donation_obj):
        return (donation_obj.created_by.id == request.user.id
                or request.user.is_admin)


class CustomPageNumberPagination(PageNumberPagination):
    """
    OVerrdiing the PAgination class to Add size field to Pagination
    """
    page_size_query_param = 'size'  # items per page


class DonationView(generics.ListCreateAPIView):
    """
    Create and Get Donation objects
    """
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filterset_fields = ['search_slug']
    serializer_class = DonationUserSerializer
    ordering = ['date_required']
    ordering_fields = ['priority']

    def get_queryset(self):
        """
        Overriding the mehtod for custom logic for admin and user
        """
        if self.request.user.is_admin:
            queryset = DonationRequest.objects.filter(
                status=Status.PENDING
            )
            return queryset
        else:
            queryset = DonationRequest.objects.filter(
                ~Q(created_by=self.request.user) &
                Q(status=Status.APPROVED)
            ).order_by('-date_required')
        return queryset


class UserRequestsView(generics.ListAPIView):
    """
    Get user's own requests
    """
    pagination_class = CustomPageNumberPagination
    serializer_class = DonationUserSerializer

    def get_queryset(self):
        """
        Overriding the mehtod for custom logic for user requests
        """
        return DonationRequest.objects.filter(created_by=self.request.user)


class DonationUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for updating and deleting a request
    """
    permission_classes = [
        IsUserAuthorized,
    ]
    queryset = DonationRequest.objects.all()
    serializer_class = DonationUserSerializer


class DonationAdminActionsView(generics.UpdateAPIView):
    """
    View for Admin Actions
    """
    permission_classes = [
        permissions.IsAdminUser,
    ]
    serializer_class = BaseSerializer
    queryset = DonationRequest.objects.all()


class BloodDonateActionView(generics.UpdateAPIView):
    """
    Donation Action View for updating the status and user
    """
    serializer_class = BloodDonateActionSerializer
    queryset = DonationRequest.objects.all()


class AwaitedDonationsViewSet(viewsets.ModelViewSet):
    """
    View set for listing soon due donation requests
    and sending alerts
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = DonationRequest.objects.all()

    def list(self, request):
        """
        List soon due donation requests
        """
        date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        queryset = DonationRequest.objects.filter(
            Q(date_required=date_tomorrow) & Q(status=Status.IN_PROGRESS))
        serializer = AwaitedDonationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def notify_donor(self, request, pk=None):
        """
        Notifies User about Soon due pending request
        """
        try:
            donation_request = self.get_object()
            send_awaited_request_notification(donation_request)
            return Response({
                "data": "Mail Sent Succesfully"
            })
        except smtplib.SMTPResponseException as e:
            print(e)
            return Response({"error": str(e)},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
