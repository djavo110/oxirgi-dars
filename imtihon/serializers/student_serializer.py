from rest_framework import serializers
from ..models import *

class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class StudentSerializer(serializers.ModelSerializer):
    # User bilan bog‘lanishi uchun
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Student
        fields = ("id", "username", "phone_number", "age", "email", "descriptions", "group", "course")
        read_only_fields = ["user"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user  # avtomatik foydalanuvchini olamiz
        course_db=validated_data.pop('course')
        user['is_active']=True
        user['is_student']=True
        user=User.objects.create_user(**user)
        student=Student.objects.create(user=user,**validated_data)
        student.course.set(course_db)
        return student

class AddUserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    is_student = serializers.BooleanField(default=False)
    is_teacher = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ["id", "username", "is_admin", "is_active", "is_student", "is_teacher"]

class StudentPostSerializer(serializers.Serializer):
    user = AddUserSerializer()
    student = StudentSerializer()

class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = "__all__"


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)
