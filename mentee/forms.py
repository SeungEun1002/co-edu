from django import forms
from .models import *
from user.models import *

class MentorSignupForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ('major', 'subject', 'teaching_subject', 'introduction')
        labels = {
            'major': '전공',
            'subject': '멘토링 가능한 분야',
            'teaching_subject': '멘토링 가능한 상세 과목',
            'introduction': '멘토 소개'
        }
        help_texts = {
            'major': '전공한 과의 이름을 작성해주세요.',
            'subject': '(멘토링 가능한 분야는 전공과 다를 수 있으며, 중복 선택 가능합니다.)',
        }


        widgets = {
            'subject': forms.CheckboxSelectMultiple(
                attrs={'style': 'vertical-align: top;'}),
            'teaching_subject': forms.Textarea(attrs={'style': 'vertical-align: top;', 'placeholder': '멘토링 가능한 과목에 대해 상세하게 작성해주세요.', 'rows': '10', 'cols': '60'}),
            'introduction': forms.Textarea(
                attrs={'style': 'vertical-align: top;', 'placeholder': '멘토로서의 자신에 대해 소개해주세요.', 'rows': '10',
                       'cols': '60'}),
        }

