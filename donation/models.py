from django.db import models
from accounts.models import BloodGroupTypes
from django.utils import timezone

class DonationRequest(models.Model):
    blood_group = models.CharField(max_length=3, choices=BloodGroupTypes.choices)
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now, db_index=True)

    def as_dict(self):
        return {'blood_group':self.blood_group, 'quantity':self.quantity, 'location':self.location, 'time': self.time}