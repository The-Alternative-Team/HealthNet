from django.contrib import admin
from .models import Appointment, Doctor, Hospital, Nurse, Patient, UserProfile, LogEntry

admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Nurse)
admin.site.register(Patient)
#admin.site.register(UserProfile)

class LogAdmin(admin.ModelAdmin):
    list_display = ('userMail', 'time', 'action')
    list_filter = ['time']
    search_fields = ['userMail', 'action']
admin.site.register(LogEntry, LogAdmin)
