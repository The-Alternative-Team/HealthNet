from django.conf.urls import url

from . import views

# app_name = 'hospital_view'
urlpatterns = [
    url(r'^$', views.index),
]
