from django.db import models
# Create your models here.
class Article(models.Model):
    link = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    create_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.subject

class Input(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    isTheSame = models.BooleanField(null=True)
    create_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.content
