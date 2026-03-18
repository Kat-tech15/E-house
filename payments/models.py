from django.db import models
from bookings.models import Booking
from users.models import CustomUser


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed')
    )
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
    