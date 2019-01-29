"""Controller

Return a tuple
(state(int): 0 is ok, context(dict))
"""
from django.contrib.auth import authenticate, login, logout


def user_login_controller(request, username, password):
    """User login controller

    Args:
        request: A HTTP request
        username(str): User name
        password(str): Password

    Returns:
         state: 0: log in successfully,
                1: user is not active,
                2: password is incorrect
    """
    state = None
    context = dict()
    user = authenticate(username=username, password=password)
    # If it fails to log in, user will be None
    if user is not None:
        # Check whether user is active
        if user.is_active:
            login(request, user)
            state = 0
        else:
            state = 1
    else:
        state = 2
    return state, context
