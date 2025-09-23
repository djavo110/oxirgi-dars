from rest_framework import serializers
from ..models import *

class TeacherPostSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "departments", "course"]

class AddUserSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(read_only=True)
    is_teacher=serializers.BooleanField(read_only=True)
    is_student=serializers.BooleanField(read_only=True)
    is_admin=serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model=User
        fields=['phone_number', 'password', 'email', 'is_active','is_teacher','is_student','is_admin', 'is_staff']

class TeacherPostSerializer(serializers.Serializer):
    user=AddUserSerializer()
    teacher=TeacherPostSSerializer()

class TeacherSerializer(serializers.ModelSerializer):
    user=AddUserSerializer()
    departments=serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all(), many=True)
    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model=Teacher
        fields = ["id", "user", "departments", "course", "descriptions"]

    def create(self, validated_data):
        user_db=validated_data.pop('user')
        departments_db=validated_data.pop('departments')
        course_db=validated_data.pop('course')

        user_db['is_active']=True
        user_db['is_teacher']=True
        user=User.objects.create_user(**user_db)

        teacher=Teacher.objects.create(user=user, **validated_data)
        teacher.departments.set(departments_db)
        teacher.course = course_db
        teacher.save()
        return teacher

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "descriptions"]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ["id", "title", "descriptions"]



