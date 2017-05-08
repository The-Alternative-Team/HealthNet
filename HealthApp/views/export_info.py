"""
Export Info view

This file contains logic regarding exporting medical info

=== Methods=== 

export_medInfo --- exports medical information and tests

"""


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect

from HealthApp import staticHelpers
from HealthApp.models import MedInfo, LogEntry, Test


@login_required(login_url="login/")
def export_medInfo(request):
    user_type, patient = staticHelpers.user_to_subclass(request.user)
    if user_type == staticHelpers.UserTypes.patient:
        export_string = "<pre>Patient: " + str(patient) + "\n\n"

        # EXPORT MEDICAL INFORMATION
        try:
            med_info = MedInfo.objects.all().filter(patient=patient)[0]
            export_string += \
                "Medical info:\n" + \
                "Date Recorded: " + med_info.time.strftime('%B %d, %Y') + "\n" + \
                "Heart Rate: " + str(med_info.heart_rate) + "\n" + \
                "Systolic Pressure: " + str(med_info.systolic_pressure) + "\n" + \
                "Diastolic Pressure: " + str(med_info.diastolic_pressure) + "\n" + \
                "Body Temperature: " + str(med_info.body_temp) + "\n" + \
                "Respiratory Rate: " + str(med_info.respiratory_rate) + "\n" + \
                "Notes: " + med_info.notes + "\n\n"
        except MedInfo.DoesNotExist:
            export_string += "No Medical Info Found.\n\n"

        # EXPORT TEST URLS
        try:
            test_list = Test.objects.all().filter(patient=patient, releaseStatus=True)

            export_string += "Test results:\n"
            for test in test_list:
                if test.releaseStatus:
                    export_string += "Test on " + test.date.strftime("%B %d, %Y") + ":\n"
                    export_string += "Notes: " + test.notes + "\n"
                    export_string += "Attached files:\n"
                    for file in test.get_attached_files():
                        export_string += "\t" + file.title + ": <a href='" + file.file.url + "' target='_blank'>" \
                                         + file.file.url + "</a>\n"
                    export_string += "\n"
        except Test.DoesNotExist:
            pass

        export_string += "</pre>"
        LogEntry.log_action(patient.username, "Exported medical information")
        return HttpResponse(export_string)
    else:
        return redirect("/")
