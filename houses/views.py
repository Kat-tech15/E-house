from rest_framework import generics, viewsets
from .models import Room, House
from .serializers import RoomSerializer, HouseSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class AvailableRoomList(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.filter(is_vacant=True)

        location = self.request.query_params.get('location')
        room_type = self.request.query_params.get('room_type')
        rent = self.request.query_params.get('rent')
        landlord =self.request.query_params.get('landlord')

        if location:
            queryset = queryset.filer(location__icontains=location)
        if room_type:
            queryset =queryset.filter(room_type=room_type)
        if rent:
            queryset = queryset.filter(rent__lte=rent)
        if landlord:
            queryset = queryset.filter(owner__username__icontains=landlord)

        return queryset

class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer