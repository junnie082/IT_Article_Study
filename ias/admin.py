from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Article, ArticleAdmin)