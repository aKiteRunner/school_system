from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('exam/', exams, name='exams'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('exam/<int:exam_id>/', exam_index, name='exam_index'),
    path('exam/<int:exam_id>/class/<int:class_id>/', class_exam, name='class_exam'),
    path('set-student-performance/', csrf_exempt(set_student_performance), name='set_student_performance'),
    path('save-students-information/', csrf_exempt(save_students_information), name='save_students_information'),
    path('create-exam/', csrf_exempt(create_exam), name='create_exam'),
    path('create-excel/<int:exam_id>', create_excel, name='create_excel')
]