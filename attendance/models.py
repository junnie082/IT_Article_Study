from django.contrib.auth.models import User
from django.db import models

from ias.models import AI, Input


class Attendance(models.Model):
    week = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    attended = models.BooleanField(null=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Week {self.week} - {self.user}"



