from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('exam/<int:exam_id>/', exam_index, name='exam_index'),
    path('exam/<int:exam_id>/class/<int:class_id>/', class_exam, name='class_exam'),
    path('set-student-performance/', set_student_performance, name='set_student_performance'),
    path('update-student-performance/', update_student_performance, name='update_student_performance'),
    path('save-students-information/', save_students_information, name='save_students_information'),
    path('create-exam/', create_exam, name='create_exam')
]