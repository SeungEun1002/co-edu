from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from user.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from mentor.models import *
from user.forms import *
from datetime import date, datetime, timedelta
from coedu.common import *
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def index(request):
    return render(request, 'mentee/layout.html')

@login_required
def mentor_signup(request):
    if request.method == 'POST':
        form = MentorSignupForm(request.POST)

        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.user = request.user
            mentor.save()
            form.save_m2m()

            #is_mentor 수정
            user=request.user
            user.is_mentor=True
            user.save()

            return redirect('mentor:index')
    else:
        form = MentorSignupForm()
    return render(request, 'mentee/mentor_signup.html', {'form': form})

@login_required
def mentee_info(request):
    if request.method == 'POST':
        form = MenteeChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mentee:mentee_info')

    form = MenteeChangeForm(instance = request.user)
    return render(request, 'mentee/mentee_info.html', {'form': form})


@login_required
def mentor_list(request):
    print(request.POST)

    # 입력 파라미터
    page = request.POST.get('page', '1')  # 페이지
    mentor_search = request.POST.get('mentor-search', '')  # 검색어
    subject_search = request.POST.getlist('subject-search', [])  # 과목 검색
    univ_search = request.POST.getlist('univ-search', [])  # 대학 검색

    qs = Mentor.objects.all()

    # qs 필터링
    ## 검색어
    qs = qs.filter(Q(user__name__icontains=mentor_search) |
                   Q(teaching_subject__icontains=mentor_search) |
                   Q(subject__name__icontains=mentor_search))

    ## 과목 검색
    if subject_search:
        qs = qs.filter(subject__code__in=subject_search)

    ## 대학 검색
    if len(univ_search) == 1:
        if 'same' in univ_search:
            qs = qs.filter(user__university=request.user.university)
        elif 'diff' in univ_search:
            qs = qs.exclude(user__university=request.user.university)

    ## 중복 제거
    qs = qs.distinct()

    # 페이징처리
    paginator = Paginator(qs, 9)  # 페이지당 9개씩 보여주기
    mentor_list = paginator.get_page(page)

    # 기타 queryset
    subject_list = Subject.objects.all()

    context = {
        'mentor_list': mentor_list,
        'subject_list': subject_list,
        'page': page,
        'mentor_search': mentor_search,
        'subject_search': subject_search,
        'univ_search': univ_search,
    }
    return render(request, 'mentee/mentor_list.html', context)


@login_required
def mentor_detail(request):
    mentor_id = request.GET.get('mentor_id')

    mentor = Mentor.objects.get(user__id=mentor_id)

    context = {
        'mentor': mentor
    }

    return render(request, 'mentee/mentor_detail.html', context)

@login_required
def mentoring_application(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        submit_btn = request.POST.get('submit_btn')

        mentoring_request = MentoringRequest.objects.get(id=id)

        if submit_btn == "취소":
            mentoring_request.status = 'cle'
            mentoring_request.save()

    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    status = request.GET.get('status', 'all')  # 필터링


    # 기본 queryset
    mentoring_waiting = MentoringRequest.objects.filter(status='ong', mentee=request.user).all()[:3]
    mentoring_request = MentoringRequest.objects.filter(mentee=request.user).exclude(status='ong')


    # 필터링
    if status != 'all':
        mentoring_request = mentoring_request.filter(status=status)

    # 검색
    if kw:
        mentoring_request = mentoring_request.filter(
            Q(mentor__user__name__icontains=kw) |  # 멘토 이름 검색
            Q(mentoring_subject__icontains=kw)  # 멘토링 내용 검색
        ).distinct()


    # 페이징처리
    paginator = Paginator(mentoring_request, 10)  # 페이지당 10개씩 보여주기
    mentoring_request = paginator.get_page(page)

    context = {
        'mentoring_waiting': mentoring_waiting,
        'mentoring_request': mentoring_request,
        'path': reverse('mentee:mentoring_application'),
        'page': page,
        'kw': kw,
        'status': status,
    }
    return render(request, 'mentee/mentoring_application.html', context)


@login_required
def mentoring_request(request):
    mentor_id = request.GET.get('mentor_id')

    mentor = Mentor.objects.get(user__id=mentor_id)

    context = {
        'mentor': mentor,
    }
    return render(request, 'mentee/mentoring_request.html', context)


@login_required
def mentee_timetable(request):
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
            request_obj = MentoringRequest.objects.filter(mentee=request.user, \
                                                          mentoring_timetable__start_datetime__gte=paging_start, \
                                                          mentoring_timetable__start_datetime__lt=paging_end, \
                                                          mentoring_timetable__start_datetime__hour=time['hour'], \
                                                          mentoring_timetable__start_datetime__week_day=weekday_num, \
                                                          status__in=['act', 'ong']).first()
            if request_obj:
                timetable_obj = request_obj.mentoring_timetable
                if request_obj.status=='act':
                    col = {
                        'obj': request_obj,
                    }
                    if timetable_obj.status == 'ong':
                        col['type'] = 'mentoringong'
                    elif timetable_obj.status == 'cpt':
                        col['type'] = 'cpt'
                elif request_obj.status=='ong':
                    col = {
                        'type': 'requestong',
                        'obj': request_obj,
                    }
            else:
                col = {
                    'type': 'empty',
                    'obj': paging_start + timedelta(days=col_idx, hours=time['hour'])
                }

            columns.append(col)
        row['columns'] = columns

        data.append(row)
    context = {
        'start': paging_start,
        'end': paging_end,
        'today': today,
        'data': data,
    }

    return render(request, 'mentee/mentee_timetable.html', context)


@login_required
def requestong_cell_modal(request):
    if request.method =='POST':
        datetime = request.POST.get('datetime')
        mentoring_request = MentoringRequest.objects.filter(mentee=request.user, mentoring_timetable__start_datetime= datetime).first()
        mentoring_request.status = 'cle'

        mentoring_request.save()
        return redirect('mentee:mentee_timetable')
    else:
        raise Http404('This view cannot get GET Request')


@login_required
def requestong_cell_modal_content(request):
    pk = request.GET.get('pk')
    mentoring_request = MentoringRequest.objects.get(id=pk)
    mentoring_timetable = mentoring_request.mentoring_timetable
    context = {
        'mentoring_request': mentoring_request,
        'mentoring_timetable': mentoring_timetable,
    }
    return render(request, 'mentee/requestong_cell_modal_content.html', context)



@login_required
def mentoringong_cell_modal(request):
    if request.method == 'POST':
        datetime = request.POST.get('datetime')
        mentoring_request = MentoringRequest.objects.filter(mentee=request.user, mentoring_timetable__start_datetime= datetime).first()
        mentoring_timetable = mentoring_request.mentoring_timetable

        mentoring_request.status = 'cle'

        mentoring_timetable.status = 'ini'
        mentoring_timetable.mentee = None
        mentoring_timetable.mentoring_subject = None
        mentoring_timetable.before_memo = None

        mentoring_request.save()
        mentoring_timetable.save()

        return redirect('mentee:mentee_timetable')
    else:
        raise Http404('This view cannot get GET Request')


@login_required
def mentoringong_cell_modal_content(request):
    pk = request.GET.get('pk')
    mentoring_request = MentoringRequest.objects.get(id=pk)
    print(mentoring_request)
    context = {
        'mentoring_request': mentoring_request,
        'mentoring_timetable': mentoring_request.mentoring_timetable
    }
    return render(request, 'mentee/mentoringong_cell_modal_content.html', context)



@login_required
def cpt_cell_modal(request):
    if request.method =='POST':
        datetime = request.POST.get('datetime')
        return redirect('mentee:mentee_timetable')
    else:
        raise Http404('This view cannot get GET Request')


@login_required
def cpt_cell_modal_content(request):
    pk = request.GET.get('pk')
    mentoring_request = MentoringRequest.objects.get(id=pk)
    context = {
        'mentoring_request': mentoring_request
    }
    return render(request, 'mentee/cpt_cell_modal_content.html', context)
