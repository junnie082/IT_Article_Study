from django.contrib import admin

# Register your models here.
from .models import Article, Input, AI


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Input)
admin.site.register(AI)