from django.contrib import admin
from .models import Employee, Profile

# Register your models here.
admin.site.register(Employee, Profile)
