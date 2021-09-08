from django.urls import path
from .views import (DonationAdminActionsView,
                    DonationView, UserRequestsView,
                    DonationUpdateDestoryView,
                    OnDonateActionView)

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
         OnDonateActionView.as_view(), name="donate_on_request")
]
