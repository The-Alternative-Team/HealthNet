from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from HealthApp.models import Message, Prescription, LogEntry
from HealthApp import staticHelpers

# This file includes the views that are used to handle ajax calls


# Marks a message as read
@login_required(login_url="login/")
def mark_read(request):
    Message.objects.get(id=request.GET["id"]).mark_read()
    return HttpResponse("Request Completed")

# Deletes a prescription
@login_required(login_url="login/")
def delete_prescription(request):
     user_type, user = staticHelpers.user_to_subclass(request.user)

     if user_type == staticHelpers.UserTypes.doctor:
        Prescription.objects.get(id=request.GET["id"]).delete()
        LogEntry.log_action(user.username, "Deleted prescription " + request.GET["id"])
        return HttpResponse("Request Completed")