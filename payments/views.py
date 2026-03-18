from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PaymentSerializer
from .models import Payment
from bookings.models import Booking


class InitiateMpesaPayment(APIView):
    
    def post(self, request):
        booking_id = request.data.get('booking_id')
        phone = request.data.get('phone_number')
        amount = request.data.get('amount')
        booking = Booking.objects.get(id=booking_id)

        payment = Payment.objects.create(
            booking=booking,
            phone=phone,
            amount=amount
        )
        stk_data = {
            'phone': phone,
            'amount':amount
        }
        response = {'message': 'STK Push sent.'}

        return Response({
            'payment_id': payment.id,
            'response': response
        })
    
class MpesaCallBack(APIView):
    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        payment_id = request.data.get('payment_id')
        payment = Payment.objects.get(id=payment_id)

        payment.transaction_id=transaction_id
        payment.status='successful'
        payment.save()

        return Response({'message': 'payment recorded successful.'})