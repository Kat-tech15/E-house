from rest_framework import generics, permissions
from .serializers import ReviewSerializer
from .models import Review


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.select_related('reviewer', 'house', 'room')
        house_id = self.request.query_params.get('house_id')
        room_id = self.request.query_params.get('room_id')

        if house_id:
            queryset = queryset.filter(house_id=house_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

        