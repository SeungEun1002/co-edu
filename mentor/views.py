from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import *
from coedu.common import *
from datetime import date, datetime, timedelta
from user.forms import *
from django.db.models import Q
from django.core.paginator import Paginator
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


    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    status = request.GET.get('status', 'ong')  # 필터링


    # 기본 queryset
    mentoring_request = MentoringRequest.objects.filter(status='ong', mentor=request.user.mentor).all()[:3]
    mentoring_timetable = MentoringTimeTable.objects.filter(mentor=request.user.mentor).exclude(status='ini').order_by('start_datetime')


    # 필터링
    if status != 'all':
        mentoring_timetable = mentoring_timetable.filter(status=status)

    # 검색
    if kw:
        mentoring_timetable = mentoring_timetable.filter(
            Q(mentee__name__icontains=kw) |  # 멘티 이름 검색
            Q(mentoring_subject__icontains=kw)  # 멘토링 내용 검색
        ).distinct()


    # 페이징처리
    paginator = Paginator(mentoring_timetable, 10)  # 페이지당 10개씩 보여주기
    mentoring_timetable = paginator.get_page(page)

    context = {
        'mentoring_request': mentoring_request,
        'mentoring_timetable': mentoring_timetable,
        'page': page,
        'kw': kw,
        'status': status,
    }
    return render(request, 'mentor/mentoring_list.html', context)

@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def mentor_timetable(request):

    time_list = get_timetable_time_list()
    cur_start, cur_end, today = get_cur_week_datetime()

    # 입력 파라미터
    paging_start = request.GET.get('start')  # 페이지
    if paging_start:
        paging_start = datetime.datetime.strptime(paging_start, '%Y-%m-%d')
    else:
        paging_start = cur_start    # 이번주

    paging_end = (paging_start + timedelta(days=6)).replace(hour=23, minute=59, second=0, microsecond=0)

    data = []
    for row_idx, time in enumerate(time_list):
        row = {
            'time_str': time['str']
        }

        weekday_num_list = [2, 3, 4, 5, 6, 7, 1]
        columns = []
        for col_idx, weekday_num in enumerate(weekday_num_list):
            timetable_obj = MentoringTimeTable.objects.filter(mentor=request.user.mentor, \
                                                              start_datetime__gte=paging_start, \
                                                              start_datetime__lt=paging_end, \
                                                              start_datetime__hour=time['hour'], \
                                                              start_datetime__week_day=weekday_num).first()
            col = {
                'type': 'full',
                'obj': timetable_obj
            }
            ##여기서 full말고 available이랑 complete도 추가해야 하는 것 아닌가?
            if not timetable_obj:
                col['type'] = 'empty'
                col['obj'] = paging_start + timedelta(days=col_idx, hours=time['hour'])

            columns.append(col)

        row['columns'] = columns

        data.append(row)
    context = {
        'start': paging_start,
        'end': paging_end,
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
def available_cell_modal(request):
    if request.method =='POST':
        datetime = request.POST.get('datetime')
        MentoringTimeTable.objects.delete(start_datetime=datetime, mentor=request.user.mentor, status='ini')

        return redirect('mentor:mentor_timetable')
    else:
        raise Http404('This view cannot get GET Request')
