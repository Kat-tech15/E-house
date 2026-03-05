from django.urls import path
from .views import RegisterView, LoginView, LogoutView, MessageListCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', MessageListCreateView.as_view(), name='contact'),
]