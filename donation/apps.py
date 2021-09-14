"""
Donation App Initialization
"""
from django.apps import AppConfig


class DonationConfig(AppConfig):
    """
    Donation App Configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donation'
