from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Renders the home page with the correct data for the current user
from django.shortcuts import render

from HealthApp import staticHelpers
from HealthApp.forms.send_message import SendMessage


def render_view(request, user_type, user):
    messages = staticHelpers.find_messages(user)
    unread_messages = staticHelpers.find_unread_messages(user)
    sendMessage = SendMessage(user_type)

    return render(request, 'HealthApp/all_messages.html',
                  {'user_type': user_type, 'messages': messages, 'unread_messages': unread_messages,
                   'sendMessage': sendMessage})


@login_required(login_url="login/")
def all_messages(request):
    user_type, user = staticHelpers.user_to_subclass(request.user)

    if user_type == staticHelpers.UserTypes.admin:
        # Redirect an admin over the admin page before trying to pull real user only data
        return redirect('/admin/')
    elif request.method == 'POST':
        if request.POST['form_id'] == 'SendMessage':
            SendMessage.handle_post(user, request.POST)

        # Form submit has been handled so redirect as a GET (this way refreshing the page works)
        return redirect('/all_messages')
    else:
        return render_view(request, user_type, user)
