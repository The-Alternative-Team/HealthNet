from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import Register, Login


@login_required(login_url="login/")
def home(request):
    return render(request, "HealthApp/patientIndex.html")


def doctor(request):
    return render(request, 'HealthApp/doctorIndex.html')


def patient(request):
    return render(request, 'HealthApp/patientIndex.html')


def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Login(request.POST)
        # check whether it's valid:
        # TODO: Check for valid data
        # if a GET (or any other method) we'll create a blank form
    else:
        form = Login()
    return render(request, 'HealthApp/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Register(request.POST)
        # check whether it's valid:
        # TODO: Check for valid data
        # if a GET (or any other method) we'll create a blank form
    else:
        form = Register()
    return render(request, 'HealthApp/register.html', {'form': form})


def blank(request):
    return render(request, 'HealthApp/blank.html')


def forms(request):
    return render(request, 'HealthApp/forms.html')


def grid(request):
    return render(request, 'HealthApp/grid.html')


def tables(request):
    return render(request, 'HealthApp/tables.html')
