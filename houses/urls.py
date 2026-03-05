from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, AvailableRoomList, HouseViewSet

router = DefaultRouter()
router.register(r'house', HouseViewSet)
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('available/rooms/', AvailableRoomList.as_view(), name='available-rooms'),
    path('', include(router.urls)),

]