from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    tenant = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'tenant', 'reviewer', 'room', 'rating', 'comment']