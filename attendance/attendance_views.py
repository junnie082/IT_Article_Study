from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from ias.models import AI
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

    attendance, due_dates = getAttendance(ai_list)  # Assuming this function returns attendance data for each article

    # Prepare rowData
    rowData = []
    for ai, ai_attendance, due_date in zip(ai_list, attendance, due_dates):
        article = ai.engSubject  # Article name
        attendance_values = ai_attendance  # Attendance values for each user
        rowData.append((ai.pk, article, due_date, attendance_values))

    rowData.reverse()
    # Paginate the queryset with 10 items per page
    paginator = Paginator(rowData, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    users = getUsers()

    context = {
        'page_obj': page_obj,  # Pass the paginated queryset to the template
        'rowData': rowData,
        'ai_list': ai_list,  # Pass the AI instances to the template
        'users': users
    }

    return render(request, 'attendance/attendance_list.html', context)
