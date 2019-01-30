"""Controller

Return a tuple
(status(int): 0 is ok, context(dict))
"""
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import ObjectDoesNotExist


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
    return page_dict


def page_slice(page, page_count):
    return slice(page_count * (page - 1), page_count * page)
