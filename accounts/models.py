from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.

class BloodGroupTypes(models.TextChoices):
    APositive = "A+"
    ANegative = "A-"
    BPositive = "B+"
    BNegative = "B-"
    OPositive = "O+"
    ONegative = "O-"
    ABPositive = "AB+"
    ABNegative = "AB-"


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, phone_number, blood_group, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Phone Number not provided')
        if not blood_group:
            raise ValueError('Blood Group Not Provided')
        
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            blood_group=blood_group,
            username=username,
            password=password
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_of_birth, phone_number, blood_group, password=None):
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
        return user

class my_user(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    blood_group = models.CharField(max_length=3, choices=BloodGroupTypes.choices, default=BloodGroupTypes.OPositive)

    objects = MyUserManager()

    REQUIRED_FIELDS = ['date_of_birth','email', 'phone_number', 'blood_group']

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
       return self.is_superuser
    def has_perm(self, perm, obj=None):
       return self.is_superuser

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin