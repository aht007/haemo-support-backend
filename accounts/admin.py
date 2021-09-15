"""
Admin Config for Accounts App
"""

from django.contrib import admin
from accounts.models import User


admin.site.register(User)
