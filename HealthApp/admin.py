"""
Admin controller

This file contains the logic behind our admin site. We register our models with the Django Admin system. 
Through the admin interface, admins can view and edit most models. 
Custom functionality for certain models is implemented below. 

Models we have included:
Doctor -------- All doctors and their profile information
Hospital ------ All hospitals and their profile information
Nurse --------- All nurses and their profile information
Patient ------- All patients and their profile information
Message ------- All messages and their contents
UploadedFile -- All files and their contents.
Appointment --- All appointments and their contents.
LogEntry ------ Displays logs for all user actions. Read only
AdminLog ------ Displays logs for Admin actions. Read only
AdmissionLog -- Used to provide statistics on patient admissions. Read only 
"""


from django.contrib import admin
from django.contrib.admin.models import LogEntry as AdminLogEntry
from .models import Appointment, Doctor, Hospital, Nurse, Patient, LogEntry, UploadedFile, Message, AdmissionLog

admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Nurse)
admin.site.register(Patient)
admin.site.register(Message)
admin.site.register(AdmissionLog)


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'uploaded_at')

admin.site.register(UploadedFile, UploadedFileAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'doctor', 'patient')

admin.site.register(Appointment, AppointmentAdmin)

# User Logs are read only. Styling included to allow filtering of all Log Entries
class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('userMail', 'time', 'action')
    list_display = ('userMail', 'time', 'action')
    list_filter = ['time']
    search_fields = ['userMail', 'action']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        # Return nothing to make sure user can't update any data
        pass

    def get_actions(self, request):
        actions = super(LogAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(LogEntry, LogAdmin)

# Admin Logs are read only and cannot be added or deleted on command.
class AdminLogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )

    list_display = ('user', 'get_action')

    def get_action(self, obj):
        return str(obj)
    get_action.short_description = 'Action'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        # Return nothing to make sure user can't update any data
        pass

    def get_actions(self, request):
        actions = super(AdminLogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(AdminLogEntry, AdminLogEntryAdmin)