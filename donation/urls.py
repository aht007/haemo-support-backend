from django.urls import path
from .views import (DonationView, ModifyDonationStatusView,
                    UserRequestsView, DonationDeleteView)

urlpatterns = [
    path('donations/', DonationView.as_view(),
         name='get_all_donation_requests'),
    path('donations/create', DonationView.as_view(),
         name='create_donation_request'),
    path('donation/edit/<int:pk>/', ModifyDonationStatusView.as_view(),
         name='modify_donation_status'),
    path('donations/requests/', UserRequestsView.as_view(),
         name='user_donations_requests'),
    path('donations/delete/<int:pk>/', DonationDeleteView.as_view(),
         name='delete_donation_request'),
]
