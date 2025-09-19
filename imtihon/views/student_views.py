from rest_framework import viewsets, status
from imtihon.models import Student
from imtihon.permissions import TeacherPermission
from imtihon.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from imtihon.serializers.student_serializer import *

class StudentApi(APIView):
    permission_classes = [TeacherPermission]
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        data["data"] = serializer.data
        return Response(data=data)

    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentsApi(APIView):
    permission_classes = [TeacherPermission]
    def get(self, request):
        parents = Parents.objects.all()
        serializer = ParentsSerializer(parents, many=True)
        data["data"] = serializer.data
        return  Response(data=data)

    @swagger_auto_schema(request_body=ParentsSerializer)
    def post(self, request):
        serializer = ParentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)