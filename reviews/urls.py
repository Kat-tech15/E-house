from django.urls import path
from .views import ReviewListCreateView

urlpatterns = [
    path('review/', ReviewListCreateView.as_view(), name='reviews_list_create'),
    path('reviews/', ReviewListCreateView.as_view(), name='reviews-list-create'),
]