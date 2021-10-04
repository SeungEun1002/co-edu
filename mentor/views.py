from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import *
# Create your views here.

def mentor_check(user):
    return user.is_mentor


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def index(request):
    return render(request, 'mentor/layout.html')

@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def mentoring_list(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        submit_btn = request.POST.get('submit_btn')

        mentoring_request = MentoringRequest.objects.get(id=id)
        if submit_btn == "수락":
            mentoring_request.status = 'act'
            mentoring_request.mentoring_timetable.status = 'ong'
            mentoring_request.mentoring_timetable.mentee = mentoring_request.mentee
            mentoring_request.mentoring_timetable.mentoring_subject = mentoring_request.mentoring_subject

            mentoring_request.save()
            mentoring_request.mentoring_timetable.save()

        else:
            mentoring_request.status = 'rej'
            mentoring_request.save()




    mentoring_request = MentoringRequest.objects.filter(status='ong', mentor=request.user.mentor).all()[:3]
    mentoring_timetable = MentoringTimeTable.objects.filter(mentor=request.user.mentor).exclude(status='ini').all()

    context = {
        'mentoring_request': mentoring_request,
        'mentoring_timetable': mentoring_timetable,
    }
    return render(request, 'mentor/mentoring_list.html', context)
