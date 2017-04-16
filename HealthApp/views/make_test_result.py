from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Renders the home page with the correct data for the current user
from django.shortcuts import render
from django.utils import timezone

from HealthApp import staticHelpers

from HealthApp.forms.send_message import SendMessage
from HealthApp.forms import UploadForm
from HealthApp.forms.create_test_result import CreateTestForm
from HealthApp.models import Message, Test, TestFile, Patient
from HealthApp.models import LogEntry


def render_view(request, user_type, user, test=None):
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
                   'create_test_form': create_test_form, 'upload_form': upload_form, 'files': files})


@login_required(login_url="login/")
def make_test_result(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real user only data
    if user_type == staticHelpers.UserTypes.admin:
        return redirect('/admin/')
    elif user_type == staticHelpers.UserTypes.patient:
        return redirect('/')
    elif request.method == 'POST':
        if request.POST['form_id'] == 'SendMessage':
            time = timezone.now()
            message = Message(subject=request.POST['subject'], body=request.POST['body'], sender=user.username,
                              recipient=request.POST['recipient'], sent_at=time)
            message.save()
            # Form submit has been handled so redirect as a GET (this way refreshing the page works)
            return redirect(request.path)
        elif request.POST['form_id'] == 'CreateTestForm':
            test = Test.objects.get(id=int(request.POST['test_id']))
            test.patient = Patient.objects.get(id=int(request.POST['patient']))
            test.date = request.POST['date']
            test.notes = request.POST['notes']
            test.save()
            LogEntry.log_action(request.user.username, "Created and completed test " + str(test.id))
            return redirect('/')
        elif request.POST['form_id'] == 'UploadForm':
            form = UploadForm(postData=request.POST, files=request.FILES)
            test = Test.objects.get(id=int(request.POST['test']))
            if form.is_valid():
                form.save()
                LogEntry.log_action(request.user.username, "Uploaded a file to test " + str(test.id))
            return render_view(request, user_type, user, test=test)
    else:
        return render_view(request, user_type, user)
