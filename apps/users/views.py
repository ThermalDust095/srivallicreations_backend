from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from rest_framework.generics import GenericAPIView
from .serializers import phoneNumberSerializer, verifyPhoneNumberSerializer
from .models import User, OTPVerification
from django.utils import timezone
from datetime import timedelta
import secrets

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_API_SECRET)

# Create your views here.
def connection_status(request):
    """
    View to check the connection status.
    """
    return JsonResponse({"status": "connected"}, status=201)

def generate_otp(user):
    code = ''.join(secrets.choice("0123456789") for _ in range(6))

    otp = OTPVerification.objects.create(
        user=user,
        otp=code,
        expires_at=timezone.now() + timedelta(minutes=settings.OTP_TIMEOUT)
    )  
    return otp

class SendOtpView(GenericAPIView):
    """
    View to send OTP to a phone number.
    """
    serializer_class = phoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone']
            try:
                user, _ = User.objects.update_or_create(phone=phone_number, is_authenticated=False)
                otp = generate_otp(user)
                message = client.messages.create(
                    body=f"Your OTP is {otp}",  # Replace with actual OTP generation logic
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=str(phone_number)
                )
                return JsonResponse({"message": "OTP sent successfully", "sid": message.sid}, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        
        return JsonResponse(serializer.errors, status=400)
    

class VerifyOTPView(GenericAPIView):
    serializer_class = verifyPhoneNumberSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            try:
                phone_number = serializer.validated_data['phone']
                user = User.objects.get(phone = phone_number)
                user.is_authenticated = True
                return JsonResponse({"message": "Authentication Sucessfull!"}, status = 200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse(serializer.errors, status=400)