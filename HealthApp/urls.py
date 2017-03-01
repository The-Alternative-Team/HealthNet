from django.conf.urls import url

from . import views

# app_name = 'HealthApp'
urlpatterns = [
    url(r'^$', views.index),
]
