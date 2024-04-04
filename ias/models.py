from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class AI(models.Model):
    subject = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_AIparagraph')

    def __str__(self):
        return self.subject

class Input(models.Model):
    ai = models.ForeignKey(AI, on_delete=models.CASCADE)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    isTheSame = models.BooleanField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='author_input')
    create_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_input')
    errCheckedStr = models.TextField(null=True)

    def __str__(self):
        return self.content
