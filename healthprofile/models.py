from accounts.models import my_user
from django.db import models

class HealthProfile(models.Model):
    user_id = models.OneToOneField(
        my_user, related_name='health_profile', on_delete=models.CASCADE)
    times_donated = models.IntegerField(default=0)

    def __str__(self):
        return self.user_id.username

class Illness(models.Model):
    medical_profile_id = models.ForeignKey(
        HealthProfile, related_name ='illness', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    date_occured = models.DateField()
    date_cured = models.DateField()

    def __str__(self):
        return self.name