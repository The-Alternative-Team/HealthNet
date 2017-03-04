from django.contrib import admin
from .models import Appointment, Doctor, Hospital, Nurse, Patient, UserProfile

admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Nurse)
admin.site.register(Patient)
admin.site.register(UserProfile)