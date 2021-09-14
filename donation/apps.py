"""
Donation App Initialization
"""
from django.apps import AppConfig


class DonationConfig(AppConfig):
    """
    Donation App configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donation'

    def ready(self):
        import donation.signals
