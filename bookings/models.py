from django.db import models
from django.db import transaction
from houses.models import Room
from users.models import CustomUser

class Booking(models.Model):
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    )
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='booking')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booking')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=BOOKING_STATUS, default='pending')
    paid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'room'],
                condition=models.Q(status='confirmed'),
                name='unique_active_booking'
            )
        ]
    
    def save(self, *args, **kwargs):
        if self.status == 'confirmed' and not self.pk:
            with transaction.atomic():
                room = Room.objects.select_for_update().get(id=self.room.id)
                if room.vacant_units <= 0:
                    raise ValueError("No vacant units available.")
                room.vacant_units -= 1
                room.save()
        super().save(*args, **kwargs)

    def confirm_booking(self):
        if self.status != 'confirmed':
            raise ValueError("Only confirmed bookings can be cancelled.")
        with transaction.atomic():
            room = Room.objects.select_for_update().get(id=self.room.id)
            room.vacant_units += 1
            room.save()
            self.status = 'cancelled'
            self.save()