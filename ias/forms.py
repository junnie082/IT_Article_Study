from django import forms
from .models import  Input, AI


class AIForm(forms.ModelForm):
    class Meta:
        model = AI
        fields = ['engSubject', 'engContent']
        labels = {
            'engSubject': 'Subject',
            'engContent': 'Content'
        }


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['content']
        labels = {
            'content': 'Content'
        }
