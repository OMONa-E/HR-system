from django.db import models
from django.contrib.auth.models import User

# Profile model
# -----------------------------------
class Profile(models.Model):
    """
    Represents a user's profile with role-based access control.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the Django `User` model.
        role (CharField): The user's role within the system. Choices include:
            - 'Admin'
            - 'Manager'
            - 'Employee' (default)

    Methods:
        __str__(): Returns a string representation of the profile, 
                   displaying the username and role.
    """
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')

    def __str__(self) -> str:
        """
        Returns:
            str: A string representation of the profile in the format 
                 "<username> - <role>".
        """
        return f'{self.user.username} - {self.role}'

# User Device model
# -----------------------------------
class UserDevice(models.Model):
    """
    Represents a user's device for token-based authentication.

    Attributes:
        user (ForeignKey): A reference to the Django `User` model, 
                           indicating which user owns the device.
        device_name (CharField): The name of the device (e.g., 'Chrome on Windows').
        refresh_token (TextField): The refresh token issued to the device.
        created_at (DateTimeField): The timestamp indicating when the device entry 
                                    was created.

    Methods:
        __str__(): Returns a string representation of the user device, 
                   displaying the username and device name.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=255)
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns:
            str: A string representation of the user device in the format 
                 "<username> - <device_name>".
        """
        return f'{self.user.username} - {self.device_name}'

# Employee model
# -----------------------------------
class Employee(models.Model):
    """
    Represents an employee's personal and job-related information.

    Attributes:
        employee_id (CharField): The employee's unique identifier (e.g., social security number).
        employee_nin (CharField): The employee's national identity number, must be unique.
        full_name (CharField): The employee's full name.
        email (EmailField): The employee's email address, must be unique.
        job_title (CharField): The employee's job title (e.g., 'Software Engineer').
        phone_number (CharField): The employee's contact phone number.
        date_joined (DateField): The date the employee joined the organization. 
                                 Automatically set to the current date.
        date_created (DateTimeField): The timestamp indicating when the employee record 
                                      was created. Automatically updated.

    Methods:
        __str__(): Returns the full name of the employee.
    """
    employee_id = models.CharField(max_length=15, unique=True) # Employee social security number
    employee_nin = models.CharField(max_length=25, unique=True) # Employee national identity number
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    job_title = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    date_joined = models.DateField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Returns:
            str: The full name of the employee.
        """
        return self.full_name


# User Profile Signals
# ---------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create a `Profile` when a new `User` is created.

    Args:
        sender (Model): The model class that triggered the signal (in this case, `User`).
        instance (User): The instance of the user being saved.
        created (bool): Whether the user instance was newly created.
        kwargs (dict): Additional keyword arguments.
    """
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal to save the `Profile` whenever the associated `User` is saved.

    Args:
        sender (Model): The model class that triggered the signal (in this case, `User`).
        instance (User): The instance of the user being saved.
        kwargs (dict): Additional keyword arguments.
    """
    instance.profile.save()
