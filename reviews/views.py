from rest_framework import generics, permissions
from .serializers import ReviewSerializer
from .models import Review

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        room_id = self.request.query_params.get('room_id', None)
        if room_id:
            return Review.objects.filter(room__id=room_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

        