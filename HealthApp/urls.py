from django.conf.urls import url

from . import views

# app_name = 'HealthApp'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^doctor', views.doctor, name="doctor"),
    url(r'^patient', views.patient, name="patient"),
    url(r'^login', views.authForm, name="login"),
    url(r'^register', views.register, name="register"),
    url(r'^blank', views.blank, name="blank"),
    url(r'^forms', views.forms, name="forms"),
    url(r'^grid', views.grid, name="grid"),
    url(r'^tables', views.tables, name="tables"),
]
