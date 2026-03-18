from django.urls import path
from .views import InitiateMpesaPayment, MpesaCallBack

urlpatterns = [
    path('initiate/', InitiateMpesaPayment.as_view(), name='initiate-payment'),
    path('callback/', MpesaCallBack.as_view(), name='mpesa-callback'),
]