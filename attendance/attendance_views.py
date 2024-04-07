from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from ias.models import AI

from attendance.models import Attendance

from attendance.function.user import getUsers, getAttendance


# Create your views here.
def attendance_list(request):
    page = request.GET.get('page', 1)  # Page number
    kw = request.GET.get('kw', '')  # Search keyword
    ai_list = AI.objects.all()
    if kw:
        ai_list = ai_list.filter(
            Q(engSubject__icontains=kw) |  # Search by subject
            Q(engContent__icontains=kw)  # Search by content
        ).distinct()

    paginator = Paginator(ai_list, 10)  # Display 10 items per page
    page_obj = paginator.get_page(page)
    users = getUsers()  # Assuming this function returns the list of users
    attendance, due_dates = getAttendance(ai_list)  # Assuming this function returns attendance data for each article

    # Prepare rowData
    rowData = []
    for id, (ai, ai_attendance, due_date) in enumerate(zip(ai_list, attendance, due_dates), start=1):
        article = ai.engSubject  # Article name
        attendance_values = ai_attendance  # Attendance values for each user
        rowData.append((id, article, due_date, attendance_values))

    context = {
        'ai_list': page_obj,
        'rowData': rowData,
        'users': users,
        'page': page,
        'kw': kw,
    }

    return render(request, 'attendance/attendance_list.html', context)
