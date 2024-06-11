from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from ias.models import AI, Input
from attendance.function.user import getUsers, getAttendance

def attendance_list(request):
    page = request.GET.get('page', 1)  # Page number
    kw = request.GET.get('kw', '')  # Search keyword
    ai_list = AI.objects.all()

    if kw:
        ai_list = ai_list.filter(
            Q(engSubject__icontains=kw) |  # Search by subject
            Q(engContent__icontains=kw)  # Search by content
        ).distinct()

    attendance, due_dates = getAttendance(ai_list)
    inputs = Input.objects.all()

    # Create a dictionary to store the largest hit value for each user in each week
    input_hit_dict = {}

    # Iterate over input objects to find the largest hit value for each user in each week
    for input_obj in inputs:
        user_id = input_obj.author.id
        week = input_obj.ai.pk

        # Update the largest hit value for the user in the current week
        input_hit_dict[(user_id, week)] = max(input_hit_dict.get((user_id, week), 0), input_obj.hit or 0)
    # Prepare rowData
    rowData = []
    for ai, ai_attendance, due_date in zip(ai_list, attendance, due_dates):
        article = ai.engSubject  # Article name
        attendance_values = ai_attendance  # Attendance values for each user

        # Get the largest hit value for the current article and week
        hit_values = [input_hit_dict.get((user.id, ai.id), 0) for user in User.objects.all()]
        print('hit_values: ' + str(hit_values))
        rowData.append((ai.pk, article, due_date, attendance_values, hit_values))

    rowData.reverse()

    # Paginate the rowData with 10 items per page
    paginator = Paginator(rowData, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Retrieve user data
    users = User.objects.all()

    context = {
        'page_obj': page_obj,  # Pass the paginated queryset to the template
        'users': users,  # Pass the user instances to the template
        'kw': kw  # Pass the search keyword to the template
    }

    return render(request, 'attendance/attendance_list.html', context)
