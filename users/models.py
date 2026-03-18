from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

import random

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord')
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Student')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, null=True, blank=True)
    email_verification_expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.username}"

    def generate_email_verification_code(self):
        self.email_verification_code = f"{random.randint(0, 999999):06d}"
        self.email_verification_expires_at = timezone.now() + timedelta(minutes=10)
        self.save(update_fields=['email_verification_code', 'email_verification_expires_at'])
        return self.email_verification_code

class Message(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.message}"
