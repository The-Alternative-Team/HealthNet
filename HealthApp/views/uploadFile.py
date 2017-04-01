from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from HealthApp.forms import UploadForm
from HealthApp.models import LogEntry


@login_required(login_url="login/")
def uploadFile(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            LogEntry.log_action(request.user.username, "Uploaded a file")
            return redirect('/')
    else:
        form = UploadForm()
    return render(request, 'HealthApp/upload.html', {
        'form': form
    })