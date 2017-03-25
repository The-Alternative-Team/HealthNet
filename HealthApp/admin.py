from django.contrib import admin
from django.contrib.admin.models import LogEntry as AdminLogEntry
from .models import Appointment, Doctor, Hospital, Nurse, Patient, LogEntry

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

class AdminLogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(AdminLogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(AdminLogEntry, AdminLogEntryAdmin)