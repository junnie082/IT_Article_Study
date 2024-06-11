from django.contrib.auth.models import User
from attendance.models import Attendance

def getUsers():
    users = list()
    for user in User.objects.all():
        users.append(user)

    return users

def getAttendance(ai_list):
    attendance_list = []
    hit_list = []
    due_dates = []

    users = User.objects.all()
    attend = Attendance.objects.all()

    for ai in ai_list:
        article_attendance = []
        due_dates.append(ai.create_date)

        for user in users:
            # Find the attendance record for the current article and user
            attendance_record = attend.filter(week=ai.id, user=user).first()

            if attendance_record:
                article_attendance.append(attendance_record.attended)
            else:
                # If no attendance record found, consider the user as absent
                article_attendance.append(False)

        attendance_list.append(article_attendance)


    return attendance_list, due_dates



