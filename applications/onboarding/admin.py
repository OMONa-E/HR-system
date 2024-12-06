from django.contrib import admin
from .models import Employee, UserDevice, Profile

# Register your models here.
admin.site.register((Employee, UserDevice, Profile))
