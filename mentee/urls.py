from django.urls import path
from .views import *

app_name = "mentee"

urlpatterns = [
    path('', index , name="index"),
    path('info/', mentee_info, name="mentee_info"),
    path('mentor/signup/', mentor_signup, name="mentor_signup"),
    path('mentor/list/', mentor_list, name="mentor_list"),
    path('mentor/detail/', mentor_detail, name="mentor_detail"),
    path('mentoring/application/', mentoring_application, name="mentoring_application"),
    path('mentoring/request/', mentoring_request, name="mentoring_request"),
    path('timetable/', mentee_timetable, name="mentee_timetable"),
]

