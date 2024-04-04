from django.contrib import admin

# Register your models here.
from .models import  Input, AI


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Input)
admin.site.register(AI)