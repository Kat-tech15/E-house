from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from .serializers import UserSerializer, LoginSerializer, VerifyEmailSerializer, EmptySerializer, MessageSerializer
from .models import CustomUser, Message

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            verification_code = user.generate_email_verification_code()

            send_mail(
                subject='Verify your Rentals account',
                message=(
                    f'Hello {user.username},\n\n'
                    f'Your verification code is: {verification_code}\n'
                    'This code expires in 10 minutes.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {'message': 'User registered successfully. Check your email for the verification code.'},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        verification_code = serializer.validated_data['verification_code']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_email_verified:
            return Response({'message': 'Email is already verified.'}, status=status.HTTP_200_OK)

        if user.email_verification_code != verification_code:
            return Response({'message': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.email_verification_expires_at or user.email_verification_expires_at < timezone.now():
            return Response({'message': 'Verification code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_email_verified = True
        user.is_active = True
        user.email_verification_code = None
        user.email_verification_expires_at = None
        user.save(
            update_fields=[
                'is_email_verified',
                'is_active',
                'email_verification_code',
                'email_verification_expires_at',
            ]
        )

        return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_email_verified:
            return Response(
                {'message': 'Please verify your email before logging in.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        if not check_password(password, user.password):
            return Response({'message': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email
        })
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    


class LogoutView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'access_token'):
            request.user.access_token.delete()

        return Response({'message': 'You have been logged out successfully.'}, status=status.HTTP_200_OK)

class MessageListCreateView(generics.GenericAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [permissions.AllowAny]