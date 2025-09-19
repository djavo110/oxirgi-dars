from rest_framework import serializers
from ..models import *


class StudentSerializer(serializers.ModelSerializer):
    # User bilan bog‘lanishi uchun
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Student
        fields = [
            "id",
            "username",
            "phone_number",
            "age",
            "email",
            "user"
        ]

    def create(self, validated_data):
        user_db = validated_data.pop("user")
        department_db = validated_data.pop("department")
        courses_db = validated_data.pop("courses")
        user_db["is_active"] = True
        user_db["is_student"] = False
        user = User.objects.create_user(**user_db)
        student = Student.objects.create(user=user, **validated_data)
        teacher.department.set(department_db)
        teacher.course.set(courses_db)
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