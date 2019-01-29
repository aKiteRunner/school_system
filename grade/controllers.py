"""Controller

Return a tuple
(status(int): 0 is ok, context(dict))
"""
from django.contrib.auth import authenticate, login, logout


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
    status = None
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
    status = None
    context = dict()
    if not request.user:
        status = 1
    else:
        status = 0
        logout(request)
    return status, context
