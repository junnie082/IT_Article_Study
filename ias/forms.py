from django import forms
from .models import  Input, AI


class AIForm(forms.ModelForm):
    class Meta:
        model = AI
        fields = ['subject', 'content']
        labels = {
            'subject': 'Subject',
            'content': 'Content'
        }


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['content']
        labels = {
            'content': 'Content'
        }
