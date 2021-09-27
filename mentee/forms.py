from django import forms
from .models import *
from user.models import *

class MentorSignupForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ('major', 'subject', 'teaching_subject', 'introduction')
        widgets = {
            "subject": forms.CheckboxSelectMultiple
        }