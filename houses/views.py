from decimal import Decimal, InvalidOperation

from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema, extend_schema_view
from rest_framework import generics, viewsets
from .models import Room, House
from .serializers import RoomSerializer, HouseSerializer


ROOM_SEARCH_PARAMETERS = [
    OpenApiParameter(
        name='location',
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description='Search by house location (contains match).',
    ),
    OpenApiParameter(
        name='category',
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description='Room category/type filter. Supports values like single_room, bedsitter, one_bedroom.',
    ),
    OpenApiParameter(
        name='room_category',
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description='Alias for category.',
    ),
    OpenApiParameter(
        name='room_type',
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description='Alias for category.',
    ),
    OpenApiParameter(
        name='type',
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description='Alias for category.',
    ),
    OpenApiParameter(
        name='rent',
        type=OpenApiTypes.DECIMAL,
        location=OpenApiParameter.QUERY,
        description='Maximum rent value (rent <= value).',
    ),
    OpenApiParameter(
        name='min_rent',
        type=OpenApiTypes.DECIMAL,
        location=OpenApiParameter.QUERY,
        description='Minimum rent value (rent >= value).',
    ),
    OpenApiParameter(
        name='max_rent',
        type=OpenApiTypes.DECIMAL,
        location=OpenApiParameter.QUERY,
        description='Maximum rent value (rent <= value).',
    ),
]


def _parse_decimal(value):
    if value in (None, ""):
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return None


def apply_room_filters(queryset, query_params):
    location = query_params.get('location')
    category = (
        query_params.get('category')
        or query_params.get('room_category')
        or query_params.get('room_type')
        or query_params.get('type')
    )
    rent = _parse_decimal(query_params.get('rent'))
    min_rent = _parse_decimal(query_params.get('min_rent'))
    max_rent = _parse_decimal(query_params.get('max_rent'))

    if location:
        queryset = queryset.filter(house__location__icontains=location)
    if category:
        queryset = queryset.filter(
            Q(type__iexact=category) | Q(category__iexact=category)
        )
    if rent is not None:
        queryset = queryset.filter(rent__lte=rent)
    if min_rent is not None:
        queryset = queryset.filter(rent__gte=min_rent)
    if max_rent is not None:
        queryset = queryset.filter(rent__lte=max_rent)

    return queryset

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related('house')
        return apply_room_filters(queryset, self.request.query_params)


RoomViewSet = extend_schema_view(
    list=extend_schema(
        parameters=ROOM_SEARCH_PARAMETERS,
        description='List rooms with optional filters for location, category/type, and rent range.',
    )
)(RoomViewSet)


class AvailableRoomList(generics.ListAPIView):
    serializer_class = RoomSerializer

    @extend_schema(
        parameters=ROOM_SEARCH_PARAMETERS,
        description='List only vacant rooms (vacant_units > 0) with optional search filters.',
    )
    def get_queryset(self):
        queryset = Room.objects.filter(vacant_units__gt=0).select_related('house')
        return apply_room_filters(queryset, self.request.query_params)

class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer