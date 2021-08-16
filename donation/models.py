from django.db import models
from accounts.models import BloodGroupTypes, User
from django.utils import timezone


class Priority(models.TextChoices):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class DonationRequest(models.Model):
    blood_group = models.CharField(
        max_length=3, choices=BloodGroupTypes.choices)
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now, db_index=True)
    created_by = models.ForeignKey(
        'accounts.User', related_name='donation_requests', on_delete=models.CASCADE)
    priority = models.CharField(max_length=6, choices=Priority.choices)

    def as_dict(self):
        return {'blood_group': self.blood_group, 'quantity': self.quantity, 'location': self.location, 'time': self.time, 'priority': self.priority}
