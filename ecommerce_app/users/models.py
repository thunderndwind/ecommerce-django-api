from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    PROFILE_CHOICES = [
        ('admin', 'Admin'),
        ('regular', 'Regular User'),
    ]
    
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    face_id = models.CharField(max_length=255, null=True, blank=True)  # Store Face ID from Azure
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=20, choices=PROFILE_CHOICES, default='regular')

    def __str__(self):
        return self.username
