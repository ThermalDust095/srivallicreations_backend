from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User, OTPVerification
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()

class phoneNumberSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True, allow_blank=False)

    def validate_phone(self, value):
        if not value.is_valid():
            raise serializers.ValidationError("Invalid phone number format.")
        return value

class verifyPhoneNumberSerializer(serializers.Serializer):
    phone = PhoneNumberField(required = True, allow_blank = False)
    otp = serializers.CharField(max_length=6)

    def validate_phone(self, value):
        try:
            user = User.objects.get(phone=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Enter a valid registered phone number")
        
        self._validated_user = user  # attach user to the serializer
        return value
    
    def validate(self, validated_data):
        user = getattr(self, "_validated_user", None)
        otp = str(validated_data.get("otp"))

        qset = OTPVerification.objects.filter(user=user).latest('created_at')
        qset.check_verification(security_code=otp)
        return validated_data
    
class UserInfoSerializer(serializers.Serializer):
    phone = serializers.CharField()
    role = serializers.SerializerMethodField()
    phone_verified = serializers.BooleanField()

    def get_role(self, obj):
        return "admin" if obj.is_admin else "customer"