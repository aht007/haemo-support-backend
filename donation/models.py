from django.db import models
from accounts.models import BloodGroupTypes
from django.utils import timezone


class Priority(models.IntegerChoices):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class DonationRequest(models.Model):
    blood_group = models.CharField(
        max_length=3, choices=BloodGroupTypes.choices)
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now, db_index=True)
    created_by = models.ForeignKey(
        'accounts.User', related_name='donation_requests',
        on_delete=models.CASCADE)
    priority = models.IntegerField(choices=Priority.choices)
    is_approved = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    description = models.CharField(max_length=500, null=True)
    comments = models.CharField(max_length=200, null=True)
    search_slug = models.SlugField(null=True)

    def as_dict(self):
        return {'blood_group': self.blood_group, 'quantity': self.quantity,
                'location': self.location, 'time': self.time,
                'priority': self.priority, 'is_approved': self.is_approved
                }
