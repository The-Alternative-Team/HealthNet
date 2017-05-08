"""
Make Test Result view

This file contains logic regarding creating and releasing test results

=== Methods=== 

render_view --- renders the modal for creating test results
make_test_result --- called when test result form is submitted

"""



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from HealthApp import staticHelpers
from HealthApp.forms import UploadForm
from HealthApp.forms.create_test_result import CreateTestForm
from HealthApp.forms.send_message import SendMessage
from HealthApp.models import LogEntry
from HealthApp.models import Test, TestFile, Patient, Message


def render_view(request, user_type, user, is_edit=False, test=None):
    unread_messages = staticHelpers.find_unread_messages(user)
    sendMessage = SendMessage(user_type)

    if test is None:
        # Delete abandoned tests
        for test in Test.objects.all().filter(patient=None):
            test.delete()

        # Create a new empty test
        test = Test(doctor=user)
        test.save()

    create_test_form = CreateTestForm(test)
    upload_form = UploadForm(test=test)
    files = TestFile.objects.all().filter(test=test)

    return render(request, 'HealthApp/make_test_result.html',
                  {'user_type': user_type, 'unread_messages': unread_messages, 'sendMessage': sendMessage,
                   'create_test_form': create_test_form, 'upload_form': upload_form, 'files': files,
                   'is_edit': is_edit})


@login_required(login_url="login/")
def make_test_result(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    if user_type == staticHelpers.UserTypes.admin:
        # Redirect an admin over the admin page before trying to pull real user only data
        return redirect('/admin/')
    elif user_type == staticHelpers.UserTypes.doctor:
        if request.method == 'POST':
            if request.POST['form_id'] == 'SendMessage':
                SendMessage.handle_post(user, request.POST)
            elif request.POST['form_id'] == 'CreateTestForm':
                test = Test.objects.get(id=int(request.POST['test_id']))
                test.patient = Patient.objects.get(id=int(request.POST['patient']))
                test.date = request.POST['date']
                test.notes = request.POST['notes']
                test.save()
                LogEntry.log_action(request.user.username, "Created or updated test " + str(test.id))

                if 'releaseStatus' in request.POST and not test.releaseStatus:
                    test.releaseStatus = True
                    test.save()
                    LogEntry.log_action(request.user.username, "Released test " + str(test.id) + " to the patient")
                    Message.sendNotifMessage(test.patient.username, "The results of your medical test have been released",
                                             str(test.doctor) + " has released the results to you.")

                return redirect('/')
            elif request.POST['form_id'] == 'UploadForm':
                form = UploadForm(postData=request.POST, files=request.FILES)
                test = Test.objects.get(id=int(request.POST['test']))
                if form.is_valid():
                    form.save()
                    LogEntry.log_action(request.user.username, "Uploaded a file to test " + str(test.id))
                return render_view(request, user_type, user, test=test)
        else:
            if 'id' in request.GET:
                test = Test.objects.get(id=int(request.GET['id']))
                if test.doctor.username == user.username:
                    return render_view(request, user_type, user, is_edit=True, test=test)
            else:
                return render_view(request, user_type, user)

    return redirect('/')
