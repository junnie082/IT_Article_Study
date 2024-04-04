from django import forms
from .models import Article, Input, AI


class AIForm(forms.ModelForm):
    class Meta:
        model = AI
        fields = ['subject', 'content']
        labels = {
            'subject': 'Subject',
            'content': 'Content'
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': 'Subject',
            'content': 'Content',
        }

class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['content']
        labels = {
            'content': 'Content'
        }
