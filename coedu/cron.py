from mentee.models import *
from mentor.models import *
from user.models import *
from coedu.common import *

from datetime import timedelta


def hour_schedule():
    _, _, now = get_cur_week_datetime()
    now = now.replace(minute=0, second=0, microsecond=0)

    # 1. 멘토링 진행중 -> 완료
    MentoringTimeTable.objects.filter()
    ongoing_timetable_list = MentoringTimeTable.objects.filter(start_datetime__lt=now, status='ong').all()
    ongoing_timetable_list.bulk_update(status='cpt')

    # 2. 멘토에게 봉사시간 1시간 추가
    for ongoing_timetable in ongoing_timetable_list:
        ongoing_timetable.mentor.service_hour += 1
        ongoing_timetable.mentor.save()

    # 3. 이전 멘토링 타임테이블 ini 삭제
    init_timetable_list = MentoringTimeTable.objects.filter(start_datetime__lt=now, status='ini').all()
    init_timetable_list.delete()

    # 4. 이전 MentoringRequest ong reject로
    ongoing_request_list = MentoringRequest.objects.filter(mentoring_timetable__start_datetime__lt=now, status='ong').all()
    ongoing_request_list.bulk_update(status='rej')
