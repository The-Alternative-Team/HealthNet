from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from HealthApp.models import MedInfo, LogEntry
from HealthApp import staticHelpers


@login_required(login_url="login/")
def export_medInfo(request):
    export_string = ""
    user_type, patient = staticHelpers.user_to_subclass(request.user)

    try:
        med_info = MedInfo.objects.all().filter(patient=patient)[0]
        if user_type == staticHelpers.UserTypes.patient:
            export_string += ("Patient: ," + med_info.patient.__str__() + "\n")
            export_string += ("Date Recorded: ," + med_info.time.strftime('%B %d, %Y') + "\n")
            export_string += ("Heart Rate: ," + str(med_info.heart_rate) + "\n")
            export_string += ("Systolic Pressure: ," + str(med_info.systolic_pressure) + "\n")
            export_string += ("Diastolic Pressure: ," + str(med_info.diastolic_pressure) + "\n")
            export_string += ("Body Temperature: ," + str(med_info.body_temp) + "\n")
            export_string += ("Respiratory Rate: ," + str(med_info.respiratory_rate) + "\n")
            export_string += ("Notes: ," + med_info.notes + "\n")
        else:
            export_string += "No Patient Found."

    except MedInfo.DoesNotExist:
        export_string += "No Medical Info Found."

    return HttpResponse(export_string)
    LogEntry.log_action(patient.username, "exported medical information")


@login_required(login_url="login/")
def export_test(request):
    return "Test Exporting coming soon to a theater near you."
    LogEntry.log_action(patient.username, "exported a test file")
