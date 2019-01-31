"""Controller

Return a tuple
(status(int): 0 is ok, context(dict))
"""
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import ObjectDoesNotExist
import pandas as pd


def user_login_controller(request, username, password):
    """User login controller

    Args:
        request: A HTTP request
        username(str): User name
        password(str): Password

    Returns:
         status(int): 0: log in successfully,
                     1: user is not active,
                     2: password is incorrect.
         context(dict): data
    """
    context = dict()
    user = authenticate(username=username, password=password)
    # If it fails to log in, user will be None
    if user is not None:
        # Check whether user is active
        if user.is_active:
            login(request, user)
            status = 0
        else:
            status = 1
    else:
        status = 2
    return status, context


def user_logout_controller(request):
    """User logout controller

    Args:
        request: A HTTP request including user information

    Returns:
        status(int): 0: log out successfully,
                    1: fails to log.
        context(dict): data
    """
    context = dict()
    if not request.user:
        status = 1
    else:
        status = 0
        logout(request)
    return status, context


def exams_controller(page, page_count=10):
    """Exams controller.

    Return all exams in a list.

    Args:
        page: the index of page.
        page_count: max number of items presented on a page.

    Returns:
        status(int): 0: query successfully,
                     1: fail to query.
        context(dict):
        {
            exams(list): [exam1, exam2, ...]
        }
    """
    context = dict()
    # Take no more than page_count exams.
    exams = Exam.objects.all().order_by('-id')[page_slice(page, page_count)]
    num_object = Exam.objects.count()
    page_dict = get_pages(num_object, page, page_count)
    status = 0
    context['exams'] = exams
    context.update(page_dict)
    return status, context


def exam_index_controller(exam_id, page, page_count=10):
    """Exam index controller.

    Return all classes which attended the exam.

    Args:
        exam_id(int): ID of the exam.
        page: the index of page.
        page_count: max number of items presented on a page.

    Returns:
        status(int): 0: query successfully.
                    1: fail to query.
        context(dict):
        {
            exam_id(int): exam_id,
            classes(list): [class1, class2, ...]
        }
    """
    context = dict()
    classes = Class.objects.all()[page_slice(page, page_count)]
    num_object = Class.objects.count()
    page_dict = get_pages(num_object, page, page_count)
    status = 0
    context['classes'] = classes
    context['exam_id'] = exam_id
    context.update(page_dict)
    return status, context


def class_grades_controller(exam_id, class_id, page, page_count=10):
    """Class grades controller

    Return all students grades of an exam in the class.

    Args:
        exam_id(int): ID of the exam.
        class_id(int): ID of the class.
        page: the index of page.
        page_count: max number of items presented on a page.

    Returns:
        status(int): 0: query successfully.
                     1: fail to query.
        context(dict):
        {
            exam_id(int): exam_id,
            class(Class): class,
            grades(list): [grade1, grade2, ...]
        }
    """
    status = None
    context = dict()
    # check whether class exists
    try:
        klass = Class.objects.get(pk=class_id)
        grades = Grade.objects.filter(student__student_class_id=class_id, exam_id=exam_id)[page_slice(page, page_count)]
        num_object = Grade.objects.filter(student__student_class_id=class_id, exam_id=exam_id).count()
        page_dict = get_pages(num_object, page, page_count)
        status = 0
        context['grades'] = grades
        context['exam_id'] = exam_id
        context['class'] = klass
        context.update(page_dict)
    except ObjectDoesNotExist:
        status = 1
    finally:
        return status, context


def all_students_controller(class_id):
    """All students in the class

    Args:
        class_id(int): ID of the class.

    Returns:
         status(int): 0: query successfully.
                     1: fail to query.
         context(dict):
        {
            students(list): [student1, student2, ...]
        }
    """
    context = dict()
    try:
        klass = Class.objects.get(pk=class_id)
        context['students'] = list(klass.student_set.all())
        status = 0
        return status, context
    except ObjectDoesNotExist:
        status = 1
        return status, context


def all_students_grades(class_id, exam_id, page, page_count=10):
    status, context = class_grades_controller(exam_id, class_id, page)
    if status == 0:
        grades = context.pop('grades')
        students = list()
        status, context2 = all_students_controller(class_id)
        all_students = context2['students']
        for grade in grades:
            student = grade.student
            all_students.remove(student)
            students.append((student.student_name, student.student_id, student.gender, grade.performance))
        for student in all_students:
            students.append((student.student_name, student.student_id, student.gender, None))
            # sort by grade
        students = sorted(students, key=lambda x: x[3] if x[3] is not None else -1, reverse=True)
        page_dict = get_pages(len(students), page, page_count)
        context['students'] = students[page_slice(page, page_count)]
        context.update(page_dict)
    else:
        status = 1
        context['message'] = '班级不存在！'
    return status, context


def update_grade(student_student_id, exam_id, performance, is_superuser=False):
    """Update a grade for the student

    Ordinary user can create but update a grade.

    Args:
        student_student_id(str): Real-life ID of the student.
        exam_id(int): ID of exam.
        performance(Decimal): Performance of the student.
        is_superuser(bool): If superuser calls this method, set it True

    Returns:
        status(int): 0: update successfully.
                     1: fail to create.
        message(str): message.
    """
    try:
        student = Student.objects.get(student_id=student_student_id)
        exam = Exam.objects.get(pk=exam_id)
        try:
            grade = Grade.objects.get(student__student_id=student_student_id, exam_id=exam_id)
            if not is_superuser:
                status = 1
                message = '该学生已有成绩！'
                return status, message
            else:
                grade.performance = performance
        except Grade.DoesNotExist:
            grade = Grade(student=student, exam=exam, performance=performance)
        grade.save()
        status = 0
        message = '操作成功'
        return status, message
    except Student.DoesNotExist:
        status = 1
        message = '学生不存在！'
        return status, message
    except Exam.DoesNotExist:
        status = 1
        message = '考试不存在！'
        return status, message


def create_exam_controller(exam_name, is_superuser=False):
    """Create an exam.

    Args:
        exam_name: Name of the exam.
        is_superuser: If superuser calls this method, set it True

    Returns:
        status(int): 0: update successfully.
                     1: fail to create.
        message(str): message.
    """
    if not is_superuser:
        status = 1
        message = '没有权限！'
        return status, message
    else:
        exam = Exam(exam_name=exam_name)
        exam.save()
        status = 0
        message = '操作成功'
        return status, message


def create_student_information(excel_file, is_superuser=False):
    """Create students information

    Args:
        excel_file: A excel file .xls or .xlsx
        is_superuser: If superuser calls this method, set it True

    Returns:
        status(int): 0: update successfully.
                     1: fail to create.
        message(str): message.
    """
    if not is_superuser:
        status = 1
        message = '没有权限！'
        return status, message
    else:
        excel_data = pd.read_excel(excel_file)
        classes = excel_data['班级']
        names = excel_data['姓名']
        ids = excel_data['学号']
        genders = excel_data['性别']
        created_class = dict()
        for class_name, name, student_id, gender in zip(classes, names, ids, genders):
            # Data type might be int or double
            class_name, name, student_id, gender = str(class_name), str(name), str(student_id), str(gender)
            # Create Class first
            if class_name not in created_class:
                try:
                    klass = Class.objects.get(class_name=class_name)
                except Class.DoesNotExist:
                    klass = Class(class_name=class_name)
                    klass.save()
                created_class[class_name] = klass
            klass = created_class[class_name]
            student = Student(student_class=klass, student_name=name, student_id=student_id, gender=gender)
            student.save()
        status = 0
        message = '操作成功'
        return status, message


def get_pages(num_object, cur_page, page_count):
    if num_object == 0:
        total_page = 1
    else:
        total_page = (num_object - 1) // page_count + 1
    page_dict = dict()
    pages = [i + 1 for i in range(total_page)]
    if cur_page > 1:
        pre_page = cur_page - 1
    else:
        pre_page = 1
    if cur_page < total_page:
        next_page = cur_page + 1
    else:
        next_page = total_page
    if cur_page <= 2:
        pages = pages[:5]
    elif total_page - cur_page <= 2:
        pages = pages[-5:]
    else:
        pages = filter(lambda x: abs(x - cur_page) <= 2, pages)
    page_dict['pages'] = pages
    page_dict['pre_page'] = pre_page
    page_dict['next_page'] = next_page
    page_dict['index_start'] = page_count * (cur_page - 1)
    return page_dict


def page_slice(page, page_count):
    return slice(page_count * (page - 1), page_count * page)
