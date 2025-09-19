from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from imtihon.models import *
from rest_framework import viewsets, status
from imtihon.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # ruxsatlarni moslab olishingiz mumkin
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:   # faqat ko‘rish uchun hamma kirishi mumkin
            return [AllowAny()]
        return [IsAuthenticated()]               # create, update, delete uchun faqat login bo‘lganlar

class StaffRegister(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = data['email']
        try:
            otp_obj = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            return Response({"error": "Bu email uchun OTP yuborilmagan"}, status=status.HTTP_400_BAD_REQUEST)

        if not otp_obj.is_verified:
            return Response({"error": "Email OTP orqali tasdiqlanmagan"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(
            email=email,
            password=data['password']
        )

        otp_obj.delete()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class Login(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Email orqali foydalanuvchini topamiz
        user = get_object_or_404(User, email=serializer.validated_data.get("email"))
        print(user)

        token = get_tokens_for_user(user)
        return Response(data=token, status=status.HTTP_200_OK)

class SendOTPView(APIView):
    @swagger_auto_schema(request_body=SentEmailSerializer)  # serializer emailni oladi
    def post(self, request):
        serializer = SentEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        if not email:
            return Response({"error": "Email kiritilishi kerak"}, status=400)

        # OTP modelidan foydalangan holda
        otp_obj, created = EmailOTP.objects.get_or_create(email=email)
        code = otp_obj.generate_otp()

        # Hozircha terminalga chiqaramiz (keyin email orqali yuborasiz)
        print(f"OTP kod: {code}")

        return Response({"message": "OTP yuborildi"}, status=200)

class VerifyOTPView(APIView):
    @swagger_auto_schema(request_body=VerifyOTPSerializer)  # bunda email + otp bo‘ladi
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_obj = serializer.validated_data["otp_obj"]
            email = serializer.validated_data["email"]

            # OTP tasdiqlash
            otp_obj.is_verified = True
            otp_obj.save()

            return Response({"message": "OTP tasdiqlandi"}, status=200)
        else:
            return Response({"error": "Xato kod kiritildi yoki muddati tugagan"}, status=400)
