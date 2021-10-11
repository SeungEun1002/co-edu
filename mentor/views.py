from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import *
from coedu.common import *
from datetime import date, datetime, timedelta
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

@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def mentor_timetable(request):

    time_list = get_timetable_time_list()
    start, end, today = get_cur_week_datetime()

    data = []
    for idx, time in enumerate(time_list):
        row = {
            'time_str': time['str']
        }

        weekday_num_list = [2, 3, 4, 5, 6, 7, 1]
        columns = []
        for weekday_num in weekday_num_list:
            timetable_obj = MentoringTimeTable.objects.filter(mentor=request.user.mentor, \
                                                              start_datetime__gte=start, \
                                                              start_datetime__lt=end, \
                                                              start_datetime__hour=time['hour'], \
                                                              start_datetime__week_day=weekday_num).first()
            columns.append(timetable_obj)

        row['columns'] = columns

        data.append(row)
    context = {
        'data': data,
    }

    return render(request, 'mentor/mentor_timetable.html', context)
