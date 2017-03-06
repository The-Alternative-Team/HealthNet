from django.conf.urls import url
from .views import home, auth, register

# app_name = 'HealthApp'
urlpatterns = [
    url(r'^$', home.home, name='home'),
    url(r'^doctor', home.home, name="doctor"),
    url(r'^patient', home.home, name="patient"),
    url(r'^login', auth.authForm, name="login"),
    url(r'^logout', auth.unauth, name="logout"),
    url(r'^register', register.register, name="register"),
]
