from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    house_name = serializers.CharField(source='house.name', read_only=True)
    room_type = serializers.CharField(source='room.type', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'reviewer',
            'reviewer_username',
            'house',
            'house_name',
            'room',
            'room_type',
            'rating',
            'comment',
            'created_at',
        ]
        read_only_fields = ['created_at']

    def validate(self, attrs):
        house = attrs.get('house')
        room = attrs.get('room')

        if house and room and room.house_id != house.id:
            raise serializers.ValidationError({'room': 'Selected room does not belong to selected house.'})

        return attrs