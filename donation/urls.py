from django.urls import path
from .views import DonationView

urlpatterns = [
    path('donations/', DonationView.as_view(), name='get_all_donation_requests')
]
