from django.conf.urls import url
from HealthApp.views import home, auth, register

# app_name = 'HealthApp'
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login', auth.authForm, name="login"),
    url(r'^logout', auth.unauth, name="logout"),
    url(r'^register', register, name="register"),
]
