from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from imtihon.models import *
from rest_framework import viewsets, status
from imtihon.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # ruxsatlarni moslab olishingiz mumkin
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:   # faqat ko‘rish uchun hamma kirishi mumkin
            return [AllowAny()]
        return [IsAuthenticated()]               # create, update, delete uchun faqat login bo‘lganlar


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class Login(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        # foydalanuvchini email + parol bilan tekshirish
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"error": "Email yoki parol xato!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"error": "Your account is disabled!"},
                status=status.HTTP_403_FORBIDDEN,
            )

        token = get_tokens_for_user(user)
        return Response(token, status=status.HTTP_200_OK)

class SendOTPView(APIView):
    @swagger_auto_schema(request_body=SentEmailSerializer)
    def post(self, request):
        serializer = SentEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        if not email:
            return Response({"error": "Email kiritilishi kerak"}, status=400)

        # OTP generatsiya qilish (cache orqali)
        import random
        from django.core.cache import cache
        from django.conf import settings
        from django.core.mail import send_mail

        otp = random.randint(100000, 999999)  # 6 xonali kod
        cache.set(f"otp_{email}", otp, timeout=300)  # 5 minut

        subject = "Sizning OTP kodingiz"
        message = f"Sizning tasdiqlash kodingiz: {otp}. Bu kod 5 daqiqa davomida amal qiladi."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return Response({"message": "OTP email orqali yuborildi"}, status=200)


class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        cached_otp = cache.get(f"otp_{email}")
        if cached_otp and str(cached_otp) == str(otp):
            # Foydalanuvchini topamiz
            user = get_object_or_404(User, email=email)
            user.is_verified = True  # modelga is_verified qo‘shib qo‘y
            user.save()

            # Cachenidagisini o‘chirib tashlaymiz
            cache.delete(f"otp_{email}")

            return Response({"success": True, "message": "Email verified successfully!"}, status=status.HTTP_200_OK)

        return Response({"success": False, "message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)