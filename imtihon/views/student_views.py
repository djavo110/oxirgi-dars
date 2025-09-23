from django.conf import settings
from rest_framework import viewsets, status
from imtihon.models import Student
from imtihon.permissions import TeacherPermission
from imtihon.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from imtihon.serializers.student_serializer import *
import random, string
from django.core.mail import send_mail

import random
import string

def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

class StudentApi(APIView):
    # permission_classes = [TeacherPermission]
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        data = serializer.data
        return Response(data=data)

    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentsApi(APIView):
    # permission_classes = [TeacherPermission]
    def get(self, request):
        parents = Parents.objects.all()
        serializer = ParentsSerializer(parents, many=True)
        data  = serializer.data
        return  Response(data=data)

    @swagger_auto_schema(request_body=ParentsSerializer)
    def post(self, request):
        serializer = ParentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminCreateStudent(APIView):
    permission_classes = [IsAdminUser]
    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 🔑 Vaqtinchalik parol yaratish
        temp_password = generate_temp_password()

        # 🔑 Student uchun user yaratish
        user = User.objects.create_user(
            email=data["email"],
            password=temp_password,
            is_student=True,
            is_active=False
        )

        # 🔑 Student modelini ham bog‘lash
        student = Student.objects.create(
            user=user,
            username=data["username"],
            phone_number=data["phone_number"],
            age=data["age"],
            email=data["email"],
            descriptions=data.get("descriptions", "")
        )

        # 🔑 Emailga login + parol yuborish
        send_mail(
            "Student Account Created",
            f"Assalomu alaykum {student.username},\n\n"
            f"Siz uchun account yaratildi.\n"
            f"Login: {student.email}\n"
            f"Parol: {temp_password}\n\n"
            "Iltimos, tizimga kirgach parolni yangilang.",
            settings.DEFAULT_FROM_EMAIL,  # DEFAULT_FROM_EMAIL ishlaydi
            [student.email],
        )

        return Response({"message": "Student yaratildi va email yuborildi"}, status=201)

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not user.is_verified:
            return Response({"error": "Email not verified!"}, status=status.HTTP_403_FORBIDDEN)

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"success": True, "message": "Password changed successfully!"}, status=status.HTTP_200_OK)