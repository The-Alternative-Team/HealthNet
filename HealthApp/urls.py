from django.conf.urls import url

from . import views

# app_name = 'HealthApp'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^doctor', views.home, name="doctor"),
    url(r'^patient', views.home, name="patient"),
    url(r'^login', views.authForm, name="login"),
    url(r'^logout', views.unauth, name="logout"),
    url(r'^register', views.register, name="register"),
]
