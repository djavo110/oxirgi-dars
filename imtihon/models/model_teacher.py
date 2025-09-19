from imtihon.models import *
from django.db import models
from imtihon.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.title

class Departments(models.Model):
    title = models.CharField( max_length=100)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField( max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    departments = models.ManyToManyField(Departments, related_name='get_department')
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="teachers", null=True, blank=True)
    descriptions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username