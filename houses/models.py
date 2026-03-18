from django.db import models
from django.core.exceptions import ValidationError
from users.models import CustomUser

class House(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    ROOM_TYPES = (
        ('single_room', 'Single_room'),
        ('bedsitter', 'Bedsitter'),
        ('double_room', 'Double_room'),
        ('one_bedroom', 'One_bedroom'),
    )
    OWNER_TYPES = (
        ('agent', 'Agent'),
        ('landlord', 'Landlord')
    )
    STATUS_CHOICES =(
        ('vacant', 'Vacant'),
        ('booked', 'Booked')
    )
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='houses')
    category = models.CharField(max_length=15, choices=OWNER_TYPES, default='landlord')
    type = models.CharField(max_length=15, choices=ROOM_TYPES, default='single_room')
    #picture = models.ImageField(upload_to='images/', blank=True,null=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_required = models.BooleanField(default=True)
    utilities_included = models.CharField(max_length=100)
    total_units  = models.IntegerField(default=0)
    vacant_units = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.house.name} - {self.type}"
    
    @property
    def status(self):
        return 'booked' if self.vacant_units == 0 else 'vacant'

    def clean(self):
        if self.vacant_units > self.total_units:
            raise ValidationError("Vacant units cannot exceed the total units")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)