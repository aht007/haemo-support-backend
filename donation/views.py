from donation.serializers import DonationSerializer
from donation.models import DonationRequest
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class IsUserAuthorized(permissions.BasePermission):
    def has_object_permission(self, request, view, donation_obj):
        return (donation_obj.created_by.id == request.user.id
                or request.user.is_admin)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'  # items per page


class DonationView(APIView):
    queryset = DonationRequest.objects.all()
    serializer_class = DonationSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request):

        if(request.user.is_admin):
            searchFilter = self.request.query_params.get('search_term')
            sortOrder = self.request.query_params.get('sortOrder')
            if(searchFilter is not None and sortOrder is not None):
                if(sortOrder == "asc"):
                    queryset = DonationRequest.objects.filter(
                        Q(is_approved=False) &
                        Q(blood_group__icontains=searchFilter)
                    ).order_by('priority')
                else:
                    queryset = DonationRequest.objects.filter(
                        Q(is_approved=False) &
                        Q(blood_group__icontains=searchFilter)
                    ).order_by('-priority')

            elif (searchFilter is not None):
                queryset = DonationRequest.objects.filter(
                    Q(is_approved=False) &
                    Q(blood_group__icontains=searchFilter)).order_by('-time')
            elif(sortOrder is not None):
                if(sortOrder == "asc"):
                    queryset = DonationRequest.objects.filter(
                        is_approved=False
                    ).order_by('priority')
                else:
                    queryset = DonationRequest.objects.filter(
                        is_approved=False
                    ).order_by('-priority')
            else:
                queryset = DonationRequest.objects.filter(
                    is_approved=False).order_by('-time')
            page = self.paginate_queryset(queryset)

        else:
            queryset = DonationRequest.objects.filter(
                is_approved=True).order_by('-time')
            page = self.paginate_queryset(queryset)

        donation_requests = DonationSerializer(
            page, context=request, many=True).data
        return self.get_paginated_response(donation_requests)

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

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


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
