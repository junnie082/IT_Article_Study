from django.urls import path

from . import views

app_name = 'discussion'

urlpatterns = [
    path('<int:ai_id>/', views.opinion_create, name='opinion_create'),
]
