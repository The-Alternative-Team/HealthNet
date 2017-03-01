from django.shortcuts import render


def index(request):
    return render(request, 'hospital_view/index.html')
