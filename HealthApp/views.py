from django.shortcuts import render


def doctor(request):
    return render(request, 'HealthApp/doctorIndex.html')


def patient(request):
    return render(request, 'HealthApp/patientIndex.html')


def login(request):
    return render(request, 'HealthApp/login.html')


def blank(request):
    return render(request, 'HealthApp/blank.html')


def forms(request):
    return render(request, 'HealthApp/forms.html')


def grid(request):
    return render(request, 'HealthApp/grid.html')


def tables(request):
    return render(request, 'HealthApp/tables.html')
