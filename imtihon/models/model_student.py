from .model_user import *
from django.db import models
from .model_teacher import *

class Student(models.Model):
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ManyToManyField('GroupStudent', related_name='get_group')
    course = models.ManyToManyField(Course, related_name="students")
    descriptions = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

class Parents(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='students')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    descriptions = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
