from rest_framework import serializers
from ..models import *
from django.contrib.auth import authenticate
from imtihon.models import EmailOTP   # email otp modeli


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number", "email", "password",  "is_student", "is_teacher", "is_active"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Foydalanuvchini tekshirish
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "success": False,
                "detail": "User does not exist"
            })

        # Parolni tekshirish
        auth_user = authenticate(email=email, password=password)
        if auth_user is None:
            raise serializers.ValidationError({
                "success": False,
                "detail": "Email or password is invalid"
            })

        # Tekshiruvdan o'tgan userni attrs ichiga joylash
        attrs["user"] = auth_user
        return attrs


class SentEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        try:
            otp_obj = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({"email": "Bunday email topilmadi"})

        if otp_obj.otp != otp or not otp_obj.is_valid():
            raise serializers.ValidationError({"otp": "OTP noto'g'ri yoki muddati tugagan"})

        # Agar hammasi to‘g‘ri bo‘lsa, otp obyektni serializer ichida saqlaymiz
        data["otp_obj"] = otp_obj
        return data