from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Question, Candidate, Comment, Hostel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from . import choices


class AskForm(forms.ModelForm):
    position = forms.ChoiceField(choices=choices.FORM_POSITION_CHOICES, initial=choices.SELECT)

    class Meta:
        model = Question
        fields = ('question', 'position', 'asked_to')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asked_to'].queryset = Question.objects.none()

        if 'position' in self.data:
            try:
                position = self.data.get('position')
                self.fields['asked_to'].queryset = Candidate.objects.filter(position=position)

            except(TypeError, ValueError):
                print(TypeError)
                print("---------")
                print(ValueError)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AnswerForm(forms.Form):
    answer = forms.CharField(widget=SummernoteWidget)

class UpdateStatsForm(forms.ModelForm):
    # name = forms.ChoiceField(choices=choices.Hostel_Names, initial=choices.SELECT)
    
    class Meta:
        model = Hostel
        fields = ('name','no_of_votes','total_residents',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))