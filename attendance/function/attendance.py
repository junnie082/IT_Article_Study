from datetime import timedelta

from attendance.models import Attendance
from django.utils import timezone

from ias.models import AI


def create_attendance(ai):
    existing_attendance = Attendance.objects.create(week=ai.id, due_date=timezone.now() + timedelta(days=7))


def update_attendance(input):
    week = input.ai.id
    user = input.author  # Assuming user is logged in

    # Check if there is an existing Attendance instance for the given week and user
    existing_attendance = Attendance.objects.filter(week=week, user=user).first()
    if existing_attendance:
        # If an existing instance is found, update it
        existing_attendance.attended = input.isTheSame
        existing_attendance.save()
    else:
        # If no existing instance is found, create a new one
        Attendance.objects.create(week=week, user=user, attended=input.isTheSame, due_date=timezone.now() + timedelta(days=7))


