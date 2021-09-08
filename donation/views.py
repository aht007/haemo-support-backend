from donation.serializers import (BaseSerializer,
                                  DonationUserSerializer,
                                  OnDonateActionSerializer)
from donation.models import DonationRequest, Status
from rest_framework import generics, permissions, parsers, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend


class IsUserAuthorized(permissions.BasePermission):
    def has_object_permission(self, request, view, donation_obj):
        return (donation_obj.created_by.id == request.user.id
                or request.user.is_admin)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'  # items per page


class DonationView(generics.ListCreateAPIView):
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filterset_fields = ['search_slug']
    serializer_class = DonationUserSerializer
    ordering = ['time']
    ordering_fields = ['priority']

    def get_queryset(self):
        if(self.request.user.is_admin):
            queryset = DonationRequest.objects.filter(
                status=Status.PENDING
            )
            return queryset
        else:
            queryset = DonationRequest.objects.filter(
                ~Q(created_by=self.request.user) &
                Q(status=Status.APPROVED)
            ).order_by('-time')
        return queryset


class UserRequestsView(generics.ListAPIView):
    pagination_class = CustomPageNumberPagination
    serializer_class = DonationUserSerializer

    def get_queryset(self):
        return DonationRequest.objects.filter(created_by=self.request.user)


class DonationUpdateDestoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsUserAuthorized,
    ]
    queryset = DonationRequest.objects.all()
    serializer_class = DonationUserSerializer


class DonationAdminActionsView(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAdminUser,
    ]
    serializer_class = BaseSerializer
    queryset = DonationRequest.objects.all()


class OnDonateActionView(generics.UpdateAPIView):
    serializer_class = OnDonateActionSerializer
    queryset = DonationRequest.objects.all()
