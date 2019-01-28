from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Exam(models.Model):
    exam_name = models.CharField(max_length=100)

    def __str__(self):
        return self.exam_name


class Class(models.Model):
    class_name = models.CharField(max_length=30)

    def __str__(self):
        return self.class_name


class Student(models.Model):
    student_name = models.CharField(max_length=40)
    gender = models.CharField(max_length=8)
    student_class = models.ForeignKey(Class, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.student_name
