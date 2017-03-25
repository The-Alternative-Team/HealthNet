from django.contrib import admin
from .models import Appointment, Doctor, Hospital, Nurse, Patient, UserProfile, LogEntry

admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Nurse)
admin.site.register(Patient)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'doctor', 'patient')


admin.site.register(Appointment, AppointmentAdmin)


class LogAdmin(admin.ModelAdmin):
    list_display = ('userMail', 'time', 'action')
    list_filter = ['time']
    search_fields = ['userMail', 'action']


admin.site.register(LogEntry, LogAdmin)
