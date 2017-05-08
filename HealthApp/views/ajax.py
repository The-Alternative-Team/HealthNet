"""
Ajax views

This file includes the views that are used to handle ajax calls

=== Methods ===
mark_read - Marks a message as read
delete_prescription - Deletes a prescription
delete_test - Deletes a test file
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from HealthApp.models import Message, Prescription, LogEntry, TestFile


# This file includes the views that are used to handle ajax calls


# Marks a message as read
@login_required(login_url="login/")
def mark_read(request):
    message = Message.objects.get(id=request.GET["id"])
    if message.recipient == request.user.username:
        message.mark_read()
    return HttpResponse("Request Completed")


# Deletes a prescription
@login_required(login_url="login/")
def delete_prescription(request):
    prescription = Prescription.objects.get(id=request.GET["id"])
    if prescription.doctor.username == request.user.username:
        prescription.delete()
        LogEntry.log_action(request.user.username, "Deleted prescription " + request.GET["id"])
        return HttpResponse("Request Completed")

# Deletes a test file
@login_required(login_url="login/")
def delete_test_file(request):
    file = TestFile.objects.get(id=request.GET["id"])
    if file.test.doctor.username == request.user.username:
        file.delete()
        LogEntry.log_action(request.user.username, "Deleted test file " + request.GET["id"])
        return HttpResponse("Request Completed")
