from django.db import models

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
