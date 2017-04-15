from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Renders the home page with the correct data for the current user
from django.shortcuts import render

from HealthApp import staticHelpers
from django.template.defaulttags import register


def render_view(request, user_type, user):
    messages = staticHelpers.find_messages(user)
    unread_messages = staticHelpers.find_unread_messages(user)

    return render(request, 'HealthApp/all_messages.html',
                  {'user_type': user_type, 'messages': messages, 'unread_messages': unread_messages})


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
    else:
        return render_view(request, user_type, user)
