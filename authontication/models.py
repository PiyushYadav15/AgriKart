from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_farmer = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True) 

