from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .forms import Register, Login, SelectAppointment, AddAppointment
from HealthApp import StaticHelpers


@login_required(login_url="login/")
def home(request):
    user_type, user = StaticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real-user only data
    if user_type == StaticHelpers.UserTypes.admin:
        return redirect('/admin/')

    events = []
    apps = StaticHelpers.find_appointments(user_type, user)

    if user_type == StaticHelpers.UserTypes.patient:
        for app in apps:
            events.append({
                'title': "Appointment with " + str(app.doctor),
                'start': str(app.start_time),
                'end': str(app.end_time)
            })
        form = SelectAppointment(user)
        addForm = AddAppointment(user_type)
        return render(request, 'HealthApp/patientIndex.html', {"events": events, 'form': form, 'addForm': addForm})
    elif user_type == StaticHelpers.UserTypes.doctor or user_type == StaticHelpers.UserTypes.nurse:
        for app in apps:
            events.append({
                'title': "Appointment with " + str(app.patient),
                'start': str(app.start_time),
                'end': str(app.end_time)
            })
        form = SelectAppointment(user)
        addForm = AddAppointment(user_type)
        return render(request, 'HealthApp/doctorIndex.html', {"events": events, 'form': form, 'addForm': addForm})


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

        userType, user = StaticHelpers.user_to_subclass(user)
        print(userType)

        return redirect('/')

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
