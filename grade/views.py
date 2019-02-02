from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from .controllers import *
from decimal import Decimal


# Create your views here.
def index(request):
    """The index of website

    Args:
        request: A HTTP request including user information.

    Returns:
        a rendered html document.
    """
    return render(request, 'index.html')


def user_login(request):
    """User login.

    Process form data submitted by user. Check whether password is correct.
    If the password is correct, user login successfully,
    else send a notice to user.

    Args:
        request: A HTTP request including user information and POST data.

    Returns:
        set user status and return to index, if login successfully.
        send a notice to user, if fail to login.
    """
    if request.method == 'POST':
        # process POST data and check password
        username = request.POST.get('username')
        password = request.POST.get('password')
        status, context = user_login_controller(request, username, password)
        if status == 0:
            # Log in successfully, redirect to index
            return redirect('index')
        elif status == 1:
            context['message'] = '用户未激活！'
        elif status == 2:
            context['message'] = '密码错误！'
        else:
            context['message'] = '未知错误！'
        return render(request, 'login.html', context)
    else:
        # If method is not POST, present login page
        return render(request, 'login.html')


@login_required
def user_logout(request):
    """User log out

    Args:
        request: A HTTP request including user information.

    Returns:
        set user status and return to index, if log out successfully.
        return to index, if user is not online (implemented by login_required).
    """
    status, context = user_logout_controller(request)
    # If log out successfully, redirect to login page,
    # else redirect to 404
    if status == 0:
        return redirect('index')
    else:
        return render(request, '404.html')


@login_required
def exams(request):
    """The index of website

        Present all exams on a page.

        Args:
            request: A HTTP request including user information.

        Returns:
            a rendered html document including a list of exams ordered reversely by date.
    """
    # Check the parameter, if page is invalid, page = 1
    page = get_page_from_request(request)
    status, context = exams_controller(page)
    return render(request, 'exams.html', context)


@login_required
def exam_index(request, exam_id):
    """Index of an exam.

    Present all the classes which attended the exam.

    Args:
        request: A HTTP request including user information.
        exam_id(int): ID of the exam.

    Returns:
         a rendered html document including a list of classes which attended the exam.
    """
    page = get_page_from_request(request)
    status, context = exam_index_controller(exam_id, page)
    return render(request, 'classes.html', context)


@login_required
def class_exam(request, exam_id, class_id):
    """Present all the students' grades of the exam in this class

    Args:
        request: A HTTP request including user information.
        exam_id(int): ID of the exam.
        class_id(int): ID of the class.

    Returns:
        A rendered html document including a list of student information.
        student information:
        {
            name: mike(str),
            student_id: 12345(str),
            gender: male(str),
            performance: 90.5(decimal)
        }
    """
    page = get_page_from_request(request)
    status, context = all_students_grades(class_id, exam_id, page)
    return render(request, 'grades.html', context)


@login_required
def set_student_performance(request):
    """Set grade of a student in an exam.

    Ordinary user can create but update a grade while superuser can do both.

    Args:
        request: A HTTP request including user information and POST data.
        request.POST:
        {
            student_student_id: 12345(str),
            exam_id: 123(str),
            performance: 90.5(str),
        }

    Returns:
        A note for user indicating whether operating successfully.
    """
    try:
        student_student_id = request.POST['student_id']
        exam_id = int(request.POST['exam_id'])
        performance = Decimal(request.POST['performance']).quantize(Decimal('0.000'))
        user = request.user
        status, message = update_grade(student_student_id, exam_id, performance, user.is_superuser)
        return HttpResponse(message)
    except (KeyError, ValueError):
        return HttpResponse('参数错误！')


@login_required
def save_students_information(request):
    """Get students information from an Excel file.

    Only administrator can call this method.

    Args:
        request: A HTTP request including user information, POST data and Excel file.
        request.FILES['excel'] is an Microsoft Excel file.
        request.POST:
        {
            class_name: 12345(str)
        }

    Returns:
        A note for user indicating whether operating successfully.
    """
    try:
        excel_file = request.FILES['excel']
        status, message = create_student_information(excel_file, request.user.is_superuser)
        context = {'message': message}
        return render(request, 'index.html', context)
    except KeyError:
        context = {'message': '请上传文件'}
        return render(request, 'index.html', context)


@login_required
def create_exam(request):
    """Create an exam.

    Only administrator can call this method.

    Args:
        request: A HTTP request including user information and POST data.
        request.POST:
        {
            exam_name: Final Exam(str)
        }

    Returns:
        A note for user indicating whether operating successfully.
    """
    try:
        exam_name = request.POST['exam_name']
        status, message = create_exam_controller(exam_name, request.user.is_superuser)
        return HttpResponse(message)
    except KeyError:
        return HttpResponse('请输入考试名称！')


@login_required
def create_excel(request, exam_id):
    """Create a zip file including grades of the exam of classes which represented in a Excel file.

    Args:
        request: A HTTP request including user information and POST data.
        exam_id: ID of the exam.

    Returns:
        a .zip file
    """
    status, zip_filename = create_excel_summary_controller(exam_id)
    zip_file = open(zip_filename, 'rb')
    response = HttpResponse(zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="%s"' % zip_file.name
    return response


def get_page_from_request(request):
    try:
        page = int(request.GET['page'])
    except (ValueError, KeyError):
        page = 1
    return page
