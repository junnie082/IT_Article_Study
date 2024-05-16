from django.urls import path

from . import views

app_name = 'discussion'

urlpatterns = [
    path('opinion/create/<int:ai_id>/', views.opinion_create, name='opinion_create'),
    path('opinion/modify/<int:opinion_id>/',
         views.opinion_modify, name='opinion_modify'),
    path('opinion/delete/<int:opinion_id>/',
         views.opinion_delete, name='opinion_delete'),
    path('opinion/vote/<int:opinion_id>/', views.opinion_vote, name='opinion_vote'),
]
