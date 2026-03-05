from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord')
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Student')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username}"

class Message(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.message}"
