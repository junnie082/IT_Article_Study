from django.urls import path

from .views import base_views, article_views, input_views

app_name = 'ias'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:article_id>/',
         base_views.detail, name='detail'),

    # article_views.py
    path('article/create/',
         article_views.article_create, name='article_create'),
    path('article/modify/<int:article_id>/',
         article_views.article_modify, name='article_modify'),
    path('article/delete/<int:article_id>/',
         article_views.article_delete, name='article_delete'),

    # input_views.py
    path('input/create/<int:article_id>/',
         input_views.input_create, name='input_create'),
    path('input/modify/<int:input_id>/',
         input_views.input_modify, name='input_modify'),
    path('input/delete/<int:input_id>/',
         input_views.input_delete, name='input_delete'),
]