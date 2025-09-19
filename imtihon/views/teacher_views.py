from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from imtihon.models import Teacher
from rest_framework.views import APIView
from imtihon.serializers import *
from imtihon.serializers.teacher_serializer import *
from imtihon.permissions import TeacherPermission

class TeacherApi(APIView):
    def get(self,request):
        data = {"success":True}
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        data["data"] = serializer.data
        return Response(data=data)

    @swagger_auto_schema(request_body=TeacherSerializer)
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseApi(APIView):
    def get(self, request):
        data = {"success":True}
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        data["data"] = serializer.data
        return Response(data=data)
    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentApi(APIView):
    def get(self, request):
        data = {"success":True}
        departments = Departments.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        data["data"] = serializer.data
        return Response(data=data)
    @swagger_auto_schema(request_body=DepartmentSerializer)
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestApi(APIView):
    permission_classes = [IsAuthenticated, TeacherPermission]

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={"success": True, "data": serializer.data})

        return Response(data={"success": False, "errors": serializer.errors})
