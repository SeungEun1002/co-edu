from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import *
from coedu.common import *
from datetime import date, datetime, timedelta
from user.forms import *
# Create your views here.

def mentor_check(user):
    return user.is_mentor


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def index(request):
    return render(request, 'mentor/layout.html')

@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def mentor_info(request):
    if request.method == 'POST':
        form = MentorChangeForm(request.POST, instance=request.user.mentor)
        if form.is_valid():
            form.save()
            return redirect('mentor:mentor_info')

    form = MentorChangeForm(instance = request.user.mentor)
    return render(request, 'mentor/mentor_info.html', {'form': form})


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
    for row_idx, time in enumerate(time_list):
        row = {
            'time_str': time['str']
        }

        weekday_num_list = [2, 3, 4, 5, 6, 7, 1]
        columns = []
        for col_idx, weekday_num in enumerate(weekday_num_list):
            timetable_obj = MentoringTimeTable.objects.filter(mentor=request.user.mentor, \
                                                              start_datetime__gte=start, \
                                                              start_datetime__lt=end, \
                                                              start_datetime__hour=time['hour'], \
                                                              start_datetime__week_day=weekday_num).first()
            if timetable_obj:
                col = {
                    'obj': timetable_obj,
                }
                if timetable_obj.status == 'ini':
                    col['type'] = 'ini'
                elif timetable_obj.status == 'ong':
                    col['type'] = 'ong'
                elif timetable_obj.status == 'cpt':
                    col['type'] = 'cpt'
            else:
                col = {
                    'type': 'empty',
                    'obj': start + timedelta(days=col_idx, hours=time['hour'])
                }


            columns.append(col)

        row['columns'] = columns

        data.append(row)
    context = {
        'start': start,
        'end': end,
        'today': today,
        'data': data,
    }

    return render(request, 'mentor/mentor_timetable.html', context)


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def empty_cell_modal(request):
    if request.method =='POST':
        datetime = request.POST.get('datetime')
        MentoringTimeTable.objects.create(start_datetime=datetime, mentor=request.user.mentor, status='ini')

        return redirect('mentor:mentor_timetable')
    else:
        raise Http404('This view cannot get GET Request')


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def ini_cell_modal(request):
    if request.method =='POST':
        datetime = request.POST.get('datetime')
        mentoring_timetable = MentoringTimeTable.objects.filter(start_datetime=datetime, mentor=request.user.mentor).first()
        mentoring_timetable.delete()
        return redirect('mentor:mentor_timetable')
    else:
        raise Http404('This view cannot get GET Request')


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def ong_cell_modal(request):
    if request.method =='POST':
        datetime = request.POST.get('datetime')
        return redirect('mentor:mentor_timetable')
    else:
        raise Http404('This view cannot get GET Request')


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def ong_cell_modal_content(request):
    pk = request.GET.get('pk')
    mentoring_timetable = MentoringTimeTable.objects.get(id=pk)
    context = {
        'mentoring_timetable': mentoring_timetable
    }
    return render(request, 'mentor/ong_cell_modal_content.html', context)


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def ong_cell_modal_content_before_memo(request):

    if request.method =='POST':
        pk = request.POST.get('pk')
        before_memo = request.POST.get('before_memo')
        mentoring_timetable = MentoringTimeTable.objects.get(id=pk)
        mentoring_timetable.before_memo = before_memo

        mentoring_timetable.save()
        return redirect('mentor:mentor_timetable')
    else:
        raise Http404('This view cannot get GET Request')




@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def cpt_cell_modal(request):
    if request.method =='POST':
        datetime = request.POST.get('datetime')
        return redirect('mentor:mentor_timetable')
    else:
        raise Http404('This view cannot get GET Request')


