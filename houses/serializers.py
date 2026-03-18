from rest_framework import serializers
from .models import House, Room

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['id', 'name', 'location', 'description', 'owner']

class RoomSerializer(serializers.ModelSerializer):
    #picture = serializers.ImageField(required=False, allow_null=True, use_url=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = ['id', 'house', 'type', 'category', 'rent', 'deposit_required', 'utilities_included', 'status']