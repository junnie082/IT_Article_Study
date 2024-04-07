from django.urls import path

from attendance import attendance_views

app_name = 'attendance'

urlpatterns = [
    path('', attendance_views.attendance_list, name='attendance_list')
]

