from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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

        LogEntry.log_action(request.user.username, "logged in")
        return redirect('/')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Login()
        return render(request, 'HealthApp/login.html', {'form': form})


def unauth(request):
    LogEntry.log_action(request.user.username, "logged out")
    logout(request)
    return redirect('/')