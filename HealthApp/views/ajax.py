from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from HealthApp.models import Message

# This file includes the views that are used to handle ajax calls


# Marks a message as read
@login_required(login_url="login/")
def mark_read(request):
    Message.objects.all().filter(id=request.GET["id"])[0].mark_read()
    return HttpResponse("Request Completed")
