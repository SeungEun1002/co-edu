from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .models import *
from coedu.common import *
from user.forms import *
from django.db.models import Q
from django.core.paginator import Paginator

from mentee.models import Chat
# Create your views here.

from datetime import date, datetime, timedelta

def mentor_check(user):
    return user.is_mentor


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def index(request):
    return render(request, 'mentor/home.html')

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
            if mentoring_request.mentoring_timetable.status == 'ini':
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
        paging_start = datetime.strptime(paging_start, '%Y-%m-%d')
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
        mentoring_timetable = MentoringTimeTable.objects.filter(start_datetime=datetime, mentor=request.user.mentor).first()
        mentoring_request = MentoringRequest.objects.filter(status='act', mentoring_timetable= mentoring_timetable).first()

        mentoring_timetable.status = 'ini'
        mentoring_timetable.mentee = None
        mentoring_timetable.mentoring_subject = None
        mentoring_timetable.before_memo = None

        mentoring_request.status = 'rej'

        mentoring_timetable.save()
        mentoring_request.save()

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


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def cpt_cell_modal_content(request):
    pk = request.GET.get('pk')
    mentoring_timetable = MentoringTimeTable.objects.get(id=pk)
    context = {
        'mentoring_timetable': mentoring_timetable
    }
    return render(request, 'mentor/cpt_cell_modal_content.html', context)


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def cpt_cell_modal_content_after_memo(request):

    if request.method =='POST':
        pk = request.POST.get('pk')
        after_memo = request.POST.get('after_memo')
        mentoring_timetable = MentoringTimeTable.objects.get(id=pk)
        mentoring_timetable.after_memo = after_memo

        mentoring_timetable.save()
        return redirect('mentor:mentor_timetable')
    else:
        raise Http404('This view cannot get GET Request')


@login_required
@user_passes_test(mentor_check, login_url='/mentee/mentor/signup/')
def mentor_chatlist(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    status = request.GET.get('status', 'all')  # 필터링

    mentee_chat_list = list()

    mentee_list = User.objects.filter(Q(chat_send__receiver=request.user) | Q(chat_receive__sender=request.user)).distinct()

    # 필터링
    if status == 'ong':
        mentee_list = mentee_list.filter(mentoringtimetable__mentor__user=request.user)
    elif status == 'cpt':
        mentee_list = mentee_list.exclude(mentoringtimetable__mentor__user=request.user)

    # 검색어
    if kw:
        mentee_list = mentee_list.filter(name__icontains=kw)

    # 페이징처리
    paginator = Paginator(mentee_list, 10)  # 페이지당 10개씩 보여주기
    mentee_list = paginator.get_page(page)

    for mentee in mentee_list:
        last_chat = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user)) \
            .filter(Q(sender=mentee) | Q(receiver=mentee)) \
            .distinct() \
            .order_by('created_datetime') \
            .last()
        if last_chat:
            mentee_chat_list.append({
                'mentee': mentee,
                'last_chat': last_chat
            })


    context = {
        'mentee_chat_list': mentee_chat_list,
        'page': page,
        'kw': kw,
        'status': status,
    }
    return render(request, 'mentor/mentor_chatlist.html', context)


@login_required
def get_chat_body(request):
    mentee_id = request.GET.get('mentee_id')

    mentee = User.objects.get(id=mentee_id)
    chat_list = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user)) \
        .filter(Q(sender=mentee) | Q(receiver=mentee)) \
        .distinct() \
        .order_by('created_datetime')

    context = {
        'mentee': mentee,
        'chat_list': chat_list,
        'chat_list_last': chat_list.last(),
    }

    return render(request, 'mentee/chat_body.html' , context)

