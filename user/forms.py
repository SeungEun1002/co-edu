from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'name', 'university', 'admission_year', 'gender', 'interest_subject')

class MenteeChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('university', 'admission_year', 'interest_subject')

class MentorChangeForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ('major', 'subject', 'teaching_subject', 'introduction')
