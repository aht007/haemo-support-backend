from donation.serializers import DonationSerializer
from donation.models import DonationRequest
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class IsUserAuthorized(permissions.BasePermission):
    def has_object_permission(self, request, view, donation_obj):
        return (donation_obj.created_by.id == request.user.id
                or request.user.is_admin)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'  # items per page


class DonationView(generics.ListCreateAPIView):
    serializer_class = DonationSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if(self.request.user.is_admin):
            searchFilter = self.request.query_params.get('search_term')
            sortOrder = self.request.query_params.get('sortOrder')
            if(searchFilter is not None and sortOrder is not None):
                if(sortOrder == "asc"):
                    queryset = DonationRequest.objects.filter(
                        Q(is_approved=False) &
                        Q(is_rejected=False) &
                        Q(searchSlug__contains=searchFilter)
                    ).order_by('priority')
                else:
                    queryset = DonationRequest.objects.filter(
                        Q(is_approved=False) &
                        Q(is_rejected=False) &
                        Q(searchSlug__contains=searchFilter)
                    ).order_by('-priority')

            elif (searchFilter is not None):
                queryset = DonationRequest.objects.filter(
                    Q(is_approved=False) &
                    Q(is_rejected=False) &
                    Q(searchSlug__contains=searchFilter)).order_by('-time')
            elif(sortOrder is not None):
                if(sortOrder == "asc"):
                    queryset = DonationRequest.objects.filter(
                        Q(is_rejected=False) &
                        Q(is_approved=False)
                    ).order_by('priority')
                else:
                    queryset = DonationRequest.objects.filter(
                        Q(is_rejected=False) &
                        Q(is_approved=False)
                    ).order_by('-priority')
            else:
                queryset = DonationRequest.objects.filter(
                    Q(is_approved=False) &
                    Q(is_rejected=False)).order_by('-time')

        else:
            queryset = DonationRequest.objects.filter(
                is_approved=True).order_by('-time')
        return queryset


class UserRequestsView(generics.ListAPIView):
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
