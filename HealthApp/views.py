from django.shortcuts import render

from .forms import Register

def doctor(request):
    return render(request, 'HealthApp/doctorIndex.html')


def patient(request):
    return render(request, 'HealthApp/patientIndex.html')


def login(request):
    return render(request, 'HealthApp/login.html')


def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Register(request.POST)
        # check whether it's valid:
            #TODO: Check for valid data
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
