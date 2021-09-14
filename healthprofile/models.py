"""
Models for Health Profile App
"""

from django.db import models


class HealthProfile(models.Model):
    """
    Health Profile Model
    """
    user_id = models.OneToOneField(
        "accounts.User", related_name='health_profile',
        on_delete=models.CASCADE)
    times_donated = models.IntegerField(default=0)

    def __str__(self):
        """
        Get String Representation
        """
        return str(self.user_id.username)


class Illness(models.Model):
    """
    Illness Model
    """
    medical_profile_id = models.ForeignKey(
        HealthProfile, related_name='illness', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    date_occured = models.DateField()
    date_cured = models.DateField()

    def __str__(self):
        """
        Get String Representation
        """
        return str(self.name)
