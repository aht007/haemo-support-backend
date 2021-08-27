from django.urls import path
from .views import (DonationView, UserRequestsView, DonationUpdateDestoryView)

urlpatterns = [
    path('donations/', DonationView.as_view(),
         name='get_all_donation_requests'),
    path('donations/create', DonationView.as_view(),
         name='create_donation_request'),
    path('donations/requests/', UserRequestsView.as_view(),
         name='user_donations_requests'),
    path('donations/<int:pk>/', DonationUpdateDestoryView.as_view(),
         name='delete_donation_request'),
]
