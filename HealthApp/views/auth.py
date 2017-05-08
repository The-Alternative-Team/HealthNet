"""
Authorization view

This file contains login and authorization logic

=== Methods=== 

authForm --- authenticates a user's credentials and logs them in
unauth --- logs a user out

"""


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from HealthApp.forms import Login
from HealthApp.models import LogEntry


def authForm(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        # if user exists and user is active, login
        if user is not None:
            if user.is_active:
                login(request, user)
                LogEntry.log_action(request.user.username, "Logged in")
                return redirect('/')

        LogEntry.log_action(email, "Failed to log in")
        # Login(True) generates an error message on the form
        return render(request, 'HealthApp/login.html', {'form': Login(True)})

        # if a GET (or any other method) we'll create a blank form
    else:
        # Login(False) generates a clean form
        return render(request, 'HealthApp/login.html', {'form': Login(False)})


def unauth(request):
    LogEntry.log_action(request.user.username, "Logged out")
    logout(request)
    return redirect('/')
