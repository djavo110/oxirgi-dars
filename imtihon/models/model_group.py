from django.db import models

from imtihon.models import Course, Teacher


class Day(models.Model):
    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

class Rooms(models.Model):
    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

class TableType(models.Model):
    title = models.CharField(max_length=100)
    descriptions = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

class Table(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(Rooms, on_delete=models.RESTRICT)
    type = models.ForeignKey(TableType, on_delete=models.RESTRICT)
    descriptions = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.start_time.__str__() + " - " + self.end_time.__str__()

class GroupStudent(models.Model):
    title = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT, related_name='course_group')
    teacher = models.ManyToManyField(Teacher, related_name='get_teacher')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    descriptions = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title