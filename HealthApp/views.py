from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .forms import Register, Login
from HealthApp import StaticHelpers


@login_required(login_url="login/")
def home(request):
    user = StaticHelpers.user_to_subclass(request.user)[1]
    user_type = StaticHelpers.user_to_subclass(request.user)[0]

    if user_type == "Patient":
        apps = StaticHelpers.find_appointments(user)
        events = []
        for app in apps:
            events.append({'title': str(app.doctor), 'start': str(app.start_time),
                           'end': str(app.end_time)})
        return render(request, 'HealthApp/patientIndex.html', events)
    elif user_type == "Doctor" or user_type == "Nurse":
        return render(request, 'HealthApp/doctorIndex.html')
    elif user_type == "Admin":
        return render(request, 'HealthApp/doctorIndex.html')


@login_required(login_url="login/")
def doctor(request):
    return render(request, 'HealthApp/doctorIndex.html')


@login_required(login_url="login/")
def patient(request):
    events = []
    """
    events.append({'title': '\nNOT AVAILABLE',
                   'start': str(app.start_time)),
                   'end': str(datetime.datetime.combine(app.date, app.end_time))})

    """
    return render(request, 'HealthApp/patientIndex.html', events)


def authForm(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        # if user exists and user is active, login
        if user is not None:
            if user.is_active:
                login(request, user)

        return redirect(request.POST['next'] + '/')

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

    # this code can be used to create endtime for the appointment
    # duration = models.IntegerField(help_text="Enter time in minutes", verbose_name='Duration')
    # end_time = start_time + datetime.timedelta(minutes = duration)
