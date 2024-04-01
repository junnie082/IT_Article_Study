from django.urls import path

from . import views

app_name = 'ias'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('input/create/<int:article_id>/', views.input_create, name='input_create'),
    path('article/create/', views.article_create, name='article_create'),
]