"""
Admin Config for health Profile App
"""
from django.contrib import admin
from healthprofile.models import HealthProfile
# Register your models here.

admin.site.register(HealthProfile)
