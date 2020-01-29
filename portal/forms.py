from django import forms
from .models import Question


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question', 'asked_to')
