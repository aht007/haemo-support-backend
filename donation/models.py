"""
Models for Donation App
"""
from django.db import models
from datetime import date
from accounts.models import BloodGroupTypes


class Priority(models.IntegerChoices):
    """
    Choices for Priority Field
    """
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Status(models.IntegerChoices):
    """
    Choices for Status Field
    """
    REJECTED = 0
    PENDING = 1
    APPROVED = 2
    IN_PROGRESS = 3
    COMPLETED = 4


class DonationRequest(models.Model):
    """
    Donation Request Model
    """
    blood_group = models.CharField(
        max_length=3, choices=BloodGroupTypes.choices)
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    date_required = models.DateField(default=date.today, db_index=True)
    created_by = models.ForeignKey(
        'accounts.User', related_name='donation_requests',
        on_delete=models.CASCADE)
    donor = models.ForeignKey(
        'accounts.User', related_name='donations',
        on_delete=models.SET_NULL, null=True
    )
    priority = models.IntegerField(choices=Priority.choices)
    status = models.IntegerField(
        choices=Status.choices, default=Status.PENDING)
    description = models.CharField(max_length=500, blank=True, default='')
    comments = models.CharField(max_length=200, blank=True, default='')
    search_slug = models.SlugField(default='')
    document = models.FileField(blank=True, null=True, default=None)
