from django.urls import path
from .views import (DonationView, UserRequestsView,
                    DonationUpdateDestoryView)

urlpatterns = [
    path('donations/', DonationView.as_view(),
         name='list_create_donation_requests'),
    path('donations/requests/', UserRequestsView.as_view(),
         name='user_donations_requests'),
    path('donations/<int:pk>/', DonationUpdateDestoryView.as_view(),
         name='update_delete_donation_request'),
]
