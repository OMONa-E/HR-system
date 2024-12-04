from django.db import models
from django.contrib.auth.models import User

# Profile model
# -----------------------------------
class Profile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')

# Employee model
# -----------------------------------
class Employee(models.Model):
    employee_id = models.CharField(max_length=15, unique=True) # Employee social security number
    employee_nin = models.CharField(max_length=25, unique=True) # Employee national identity number
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    job_title = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    date_joined = models.DateField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.full_name


# User Profile Signals
# ---------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
