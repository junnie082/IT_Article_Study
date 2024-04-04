from django.urls import path

from .views import base_views, input_views, ai_views

app_name = 'ias'

urlpatterns = [
    # base_views.py
    path('',
         base_views.ai_index, name='ai_index'),
    path('<int:ai_id>/',
         base_views.ai_detail, name='ai_detail'),

    # ai_views.py
    path('ai/create/',
         ai_views.ai_create, name='ai_create'),

    # input_views.py
    path('input/create/<int:ai_id>/',
         input_views.input_create, name='input_create'),
    path('input/modify/<int:input_id>/',
         input_views.input_modify, name='input_modify'),
    path('input/delete/<int:input_id>/',
         input_views.input_delete, name='input_delete'),
    path('input/vote/<int:input_id>/', input_views.input_vote, name='input_vote'),

]