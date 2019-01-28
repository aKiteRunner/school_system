from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Exam(models.Model):
    """ Class for exam.

    Attributes:
        exam_name (str): A string representing exam full name.
    """
    exam_name = models.CharField(max_length=100)

    def __str__(self):
        return self.exam_name


class Class(models.Model):
    """ Class for class.

    A class has many students.

    Attributes:
        class_name (str): A string representing class name
    """
    class_name = models.CharField(max_length=30)

    def __str__(self):
        return self.class_name


class Student(models.Model):
    """ Class for student.

    Attributes:
        student_name (str): A string representing student name.
        gender (str): A string representing student gender.
        student_class (Class): A foreign key to Class indicating class the student belongs to.
        student_id (str): A string representing student id in real life.
    """
    student_name = models.CharField(max_length=40)
    gender = models.CharField(max_length=8)
    student_class = models.ForeignKey(Class, on_delete=models.DO_NOTHING)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.student_name


class Grade(models.Model):
    """ Grade of each student for every exam.

    Each student has a grade in one exam.

    Attributes:
        student (Student): A foreign key to Student.
        exam (Exam): A foreign key to Exam.
        performance (int): A integer indicating the grade of a student.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    performance = models.IntegerField()
