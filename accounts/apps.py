"""
Account Application Initialization
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration for Accounts App
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
