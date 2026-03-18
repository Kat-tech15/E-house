from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, LogoutView, MessageListCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', MessageListCreateView.as_view(), name='contact'),
]