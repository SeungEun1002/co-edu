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
    path('mentoring_request_modal/content/', mentoring_request_modal_content, name="mentoring_request_modal_content"),
    path('mentoring_request_modal/', mentoring_request_modal, name="mentoring_request_modal"),
    path('mentoring/request/', mentoring_request, name="mentoring_request"),
    path('chatlist/', mentee_chatlist, name="mentee_chatlist"),
    path('timetable/', mentee_timetable, name="mentee_timetable"),
    path('requestong_cell_modal/content/', requestong_cell_modal_content, name="requestong_cell_modal_content"),
    path('requestong_cell_modal/', requestong_cell_modal, name="requestong_cell_modal"),
    path('mentoringong_cell_modal/content/', mentoringong_cell_modal_content, name="mentoringong_cell_modal_content"),
    path('mentoringong_cell_modal/', mentoringong_cell_modal, name="mentoringong_cell_modal"),
    path('cpt_cell_modal/content/', cpt_cell_modal_content, name="cpt_cell_modal_content"),
    path('cpt_cell_modal/', cpt_cell_modal, name="cpt_cell_modal"),
    path('send/chat/', send_chat, name="send_chat"),

]

