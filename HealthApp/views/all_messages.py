from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Renders the home page with the correct data for the current user
from django.shortcuts import render
from django.utils import timezone

from HealthApp import staticHelpers
from django.template.defaulttags import register

from HealthApp.forms.send_message import SendMessage
from HealthApp.models import Message


def render_view(request, user_type, user):
    messages = staticHelpers.find_messages(user)
    unread_messages = staticHelpers.find_unread_messages(user)
    sendMessage = SendMessage(user_type)

    return render(request, 'HealthApp/all_messages.html',
                  {'user_type': user_type, 'messages': messages, 'unread_messages': unread_messages, 'sendMessage': sendMessage})


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
    # Called when the home view is loaded or a form is submitted  # Called when the home view is loaded or a form is
    # submitted


@login_required(login_url="login/")
def all_messages(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    # Redirect an admin over the admin page before trying to pull real user only data
    if user_type == staticHelpers.UserTypes.admin:
        return redirect('/admin/')
    elif request.method == 'POST':
        if request.POST['form_id'] == 'SendMessage':
            time = timezone.now()
            message = Message(subject=request.POST['subject'], body=request.POST['body'], sender=user.username,
                              recipient=request.POST['recipient'], sent_at=time)
            message.save()
            # Form submit has been handled so redirect as a GET (this way refreshing the page works)
            return redirect('/')
    else:
        return render_view(request, user_type, user)
