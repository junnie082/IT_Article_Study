from django.urls import path

from . import views
from .views import transcribe_audio, interrupt

# from .views import transcribe_audio

app_name = 'voice'

urlpatterns = [
    # Other URL patterns
    path('transcribe/<int:ai_id>/', transcribe_audio, name='transcribe_audio'),
    path('transcribe/interrupt/', interrupt, name='interrupt')
]
