from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .controllers import *


# Create your views here.
@login_required
def index(request):
    """The index of website

    Present all exams on a page.

    Args:
        request: A HTTP request including user information.

    Returns:
        a rendered html document including a list of exams ordered reversely by date.
    """
    # TODO: implement this function
    return render(request, 'index.html')


def user_login(request):
    """User login.

    Process form data submitted by user. Check whether password is correct.
    If the password is correct, user login successfully,
    else send a notice to user.

    Args:
        request: A HTTP request including user information and POST data.

    Returns:
        set user state and return to index, if login successfully.
        send a notice to user, if fail to login.
    """
    if request.method == 'POST':
        # process POST data and check password
        username = request.POST.get('username')
        password = request.POST.get('password')
        state, context = user_login_controller(request, username, password)
        if state == 0:
            # Log in successfully, redirect to index
            return redirect('index')
        elif state == 1:
            context['message'] = '用户未激活！'
        elif state == 2:
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
        set user state and return to index, if log out successfully.
        return to index, if user is not online (implemented by login_required).
    """
    state, context = user_logout_controller(request)
    # If log out successfully, redirect to login page,
    # else redirect to 404
    if state == 0:
        return redirect('user_login')
    else:
        return render(request, '404.html')


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
    pass


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
    pass


@login_required
def set_student_performance(request):
    """Set grade of a student in an exam.

    Args:
        request: A HTTP request including user information and POST data.
        request.POST:
        {
            student_id: 12345(str),
            exam_id: 123(str),
            performance: 90.5(str),
        }

    Returns:
        A note for user indicating whether operating successfully.
    """
    pass


@login_required
def update_student_performance(request):
    """Update grade of a student in an exam.

    Only administrator can call this method.

    Args:
        request: A HTTP request including user information and POST data.
        request.POST:
        {
            student_id: 12345(str),
            exam_id: 123(str),
            performance: 90.5(str)
        }

    Returns:
        A note for user indicating whether operating successfully.
    """
    pass


@login_required
def save_students_information(request):
    """Get students information from an Excel file.

    Only administrator can call this method.

    Args:
        request: A HTTP request including user information, POST data and Excel file.
        request.FILE is an Microsoft Excel file.
        request.POST:
        {
            class_name: 12345(str)
        }

    Returns:
        A note for user indicating whether operating successfully.
    """
    pass


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
    pass
