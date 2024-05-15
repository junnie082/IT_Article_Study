from django.contrib.auth.models import User
from ias.models import AI
from django.db import models
# Create your models here.

class Opinion(models.Model):
    ai = models.ForeignKey(AI, on_delete=models.CASCADE)
    opinion = models.TextField(null=True)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_opinion')
    voter = models.ManyToManyField(User, related_name='voter_Opinion')

    def __str__(self):
        return self.ai.engSubject + " - " + self.opinion