from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from HealthApp import staticHelpers
from HealthApp.models import MedInfo, LogEntry, Test, TestFile


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

    LogEntry.log_action(patient.username, "exported medical information")
    return HttpResponse(export_string)


@login_required(login_url="login/")
def export_test(request):
    user_type, patient = staticHelpers.user_to_subclass(request.user)
    try:
        test_list = Test.objects.all().filter(patient=patient, releaseStatus=True)
    except Test.DoesNotExist:
        test_list = []
    for test in test_list:
        try:
            file = ((TestFile.objects.all().filter(test=test))[0]).file
        except TestFile.DoesNotExist:
            file = ""

    LogEntry.log_action(request.user.username, "exported a test file")
    return HttpResponse(file)
