from donation.serializers import (BaseSerializer,
                                  DonationUserSerializer,
                                  DonationInProgressActionSerializer)
from donation.models import DonationRequest
from rest_framework import generics, permissions, parsers
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class IsUserAuthorized(permissions.BasePermission):
    def has_object_permission(self, request, view, donation_obj):
        return (donation_obj.created_by.id == request.user.id
                or request.user.is_admin)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'  # items per page


class DonationView(generics.ListCreateAPIView):
    pagination_class = CustomPageNumberPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filterset_fields = ['search_slug']
    serializer_class = DonationUserSerializer

    def get_queryset(self):
        if(self.request.user.is_admin):
            sortOrder = self.request.query_params.get('sortOrder')
            if(sortOrder is not None):
                if(sortOrder == "asc"):
                    queryset = DonationRequest.objects.filter(
                        Q(is_approved=False) &
                        Q(is_rejected=False) &
                        Q(in_progress=False)
                    ).order_by('priority')
                else:
                    queryset = DonationRequest.objects.filter(
                        Q(is_approved=False) &
                        Q(is_rejected=False) &
                        Q(in_progress=False)
                    ).order_by('-priority')

            else:
                queryset = DonationRequest.objects.filter(
                    Q(is_approved=False) &
                    Q(is_rejected=False) &
                    Q(in_progress=False)).order_by('-time')

        else:
            queryset = DonationRequest.objects.filter(
                ~Q(created_by=self.request.user) &
                Q(is_approved=True) &
                Q(in_progress=False)).order_by('-time')
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


class DonationInProgressActionView(generics.UpdateAPIView):
    serializer_class = DonationInProgressActionSerializer
    queryset = DonationRequest.objects.all()
