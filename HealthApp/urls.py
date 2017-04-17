from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from HealthApp.views import home, auth, register, all_patients, admitted_patients, all_messages, ajax, make_test_result

# app_name = 'HealthApp'
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login', auth.authForm, name="login"),
    url(r'^logout', auth.unauth, name="logout"),
    url(r'^register', register, name="register"),
    url(r'^all_patients', all_patients, name="all_patients"),
    url(r'^admitted_patients', admitted_patients, name="admitted_patients"),
    url(r'^all_messages', all_messages, name="all_messages"),
    url(r'^make_test_result', make_test_result, name="make_test_result"),
    url(r'^ajax/mark_read', ajax.mark_read, name="mark_read"),
    url(r'^ajax/delete_prescription', ajax.delete_prescription, name="delete_prescription"),
]

# Add the uploaded files to the URLs
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
