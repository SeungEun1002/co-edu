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
        labels = {
            'username': 'ID',
            'name': '이름',
            'university': '대학교',
            'admission_year': '입학년도',
            'gender': '성별',
            'interest_subject': '관심있는 분야',
        }
        help_texts = {
            'name': '정확한 이름을 한글로 입력해주세요.',
            'university': '띄어쓰기 없이 공식적인 대학명을 입력해주세요. ex)성대(X), 성균관대학교(O)',
            'interest_subject': '멘토링 받고 싶은 관심분야에 대해 자세히 작성해주세요.',
        }


class MenteeChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('university', 'admission_year', 'interest_subject')
        labels = {
            'university': '대학교',
            'admission_year': '입학년도',
            'interest_subject': '관심있는 분야',
        }
        help_texts = {
            'name': '정확한 이름을 한글로 입력해주세요.',
            'university': '띄어쓰기 없이 공식적인 대학명을 입력해주세요. ex)성대(X), 성균관대학교(O)',
            'interest_subject': '멘토링 받고 싶은 관심분야에 대해 자세히 작성해주세요.',
        }



class MentorChangeForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ('major', 'subject', 'teaching_subject', 'introduction')
        labels = {
            'major': '전공',
            'subject': '멘토링 가능한 분야',
            'teaching_subject': '멘토링 가능한 상세 과목',
            'introduction': '멘토로서 소개'
        }
        help_texts = {
            'major': '전공한 과의 이름을 작성해주세요.',
            'subject': '멘토링 가능한 분야는 전공과 다를 수 있으며, 중복 선택 가능합니다.',
            'teaching_subject': '멘토링 가능한 과목에 대해 상세하게 작성해주세요.',
            'introduction': '멘토로서의 자신에 대해 소개해주세요.'
        }

