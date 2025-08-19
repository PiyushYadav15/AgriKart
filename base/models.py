from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
# Create your models here.
# User model (extended)
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): 
        return self.name
    

# Crop model
class Crop(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='crops/')
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_available = models.FloatField()
    listed_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted=models.BooleanField(default=False)

# Order model
class Order(models.Model):
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity_ordered = models.FloatField()
    delivery_address = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    status = models.CharField(
        choices=[
            ('pending', 'Pending'),
            ('packed', 'Packed'),
            ('delivered', 'Delivered')
        ],
        default='pending',
        max_length=20
    )

    def __str__(self):
        return f"{self.crop.name} - {self.consumer.username if self.consumer else 'Guest'} - {self.status}"
    
class Notification(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer_notifications',null=True)
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consumer_notifications', null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE,null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.farmer.username}"
    


