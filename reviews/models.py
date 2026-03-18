from django.db import models
from users.models import CustomUser
from houses.models import Room

class Review(models.Model):
    reviewer = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms')
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'room')