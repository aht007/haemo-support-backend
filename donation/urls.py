"""
Urls for Donation App
"""
from django.urls import path
from rest_framework import routers

from .views import (DonationAdminActionsView,
                    DonationView, UserRequestsView,
                    DonationUpdateDestoryView,
                    BloodDonateActionView, AwaitedDonationsViewSet,
                    PendingDonationsViewSet)

router = routers.DefaultRouter()
router.register(r'awaited-donations', AwaitedDonationsViewSet, 'donations')
router.register(r'due-soon-pending-donations',
                PendingDonationsViewSet, 'donations')

urlpatterns = [
    path('donations/', DonationView.as_view(),
         name='list_create_donation_requests'),
    path('donations/requests/', UserRequestsView.as_view(),
         name='user_donations_requests'),
    path('donations/<int:pk>/', DonationUpdateDestoryView.as_view(),
         name='update_delete_donation_request'),
    path('donations/<int:pk>/approve/',
         DonationAdminActionsView.as_view(), name="donation_approve"),
    path('donations/<int:pk>/reject/',
         DonationAdminActionsView.as_view(), name="donation_reject"),
    path('donations/<int:pk>/donate/',
         BloodDonateActionView.as_view(), name="donate_on_request")
]

urlpatterns += router.urls
