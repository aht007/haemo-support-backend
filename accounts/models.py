"""
Models for Accounts App
"""

from django.db.models import signals
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

from healthprofile.models import HealthProfile


class BloodGroupTypes(models.TextChoices):
    """
    Blood Group Choices for blood group field
    """
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"


class UserManager(BaseUserManager):
    """
    Custom User Manager
    """

    def create_user(self, username, email, date_of_birth,
                    phone_number, blood_group=None, password=None,
                    is_admin=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Phone Number not provided')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            blood_group=blood_group,
        )
        if is_admin is True:
            user.is_admin = True
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        # initialize user's health profile
        HealthProfile.objects.create(
            user_id=user
        )
        return user

    def create_superuser(self, username, email, date_of_birth, phone_number,
                         blood_group=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            blood_group=blood_group
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        # initialize user's health profile
        return user


class User(AbstractUser):
    """
    Custom User Class
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered"
        "in the format: '+999999999'. Up to 15 digits allowed.")

    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # validators should be a list
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    blood_group = models.CharField(
        max_length=3, choices=BloodGroupTypes.choices, null=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['date_of_birth', 'email', 'phone_number', 'blood_group']

    def __str__(self):
        """
        return string representation of user model
        """
        return self.email

    def has_module_perms(self, app_label):
        """
        check if user has module permission
        """
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        """
        check if user has permission
        """
        return self.is_superuser

    @property
    def is_staff(self):
        """
        Check if user is staff member
        """
        return self.is_admin
