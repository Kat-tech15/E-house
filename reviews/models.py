from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
from houses.models import House, Room

class Review(models.Model):
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'room')

    def __str__(self):
        return f"{self.reviewer.username} - {self.room.type} ({self.rating} stars)"