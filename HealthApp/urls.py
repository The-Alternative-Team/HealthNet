from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from HealthApp.views import home, auth, register, uploadFile

# app_name = 'HealthApp'
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login', auth.authForm, name="login"),
    url(r'^logout', auth.unauth, name="logout"),
    url(r'^register', register, name="register"),
    url(r'^upload$', uploadFile, name="upload_form"),
]

# Add the uploaded files to the URLs
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
