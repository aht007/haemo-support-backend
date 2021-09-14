"""
Django Admin Config for Donation App
"""
from django.contrib import admin
from donation.models import DonationRequest


admin.site.register(DonationRequest)
