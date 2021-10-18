from django.urls import path
from .views import *

app_name = "mentor"

urlpatterns = [
    path('', index , name="index"),
    path('info/', mentor_info, name="mentor_info"),
    path('mentoring/', mentoring_list , name="mentoring_list"),
    path('chatlist/', mentor_chatlist, name="mentor_chatlist"),
    path('timetable/', mentor_timetable, name="mentor_timetable"),
    path('empty_cell_modal/', empty_cell_modal, name="empty_cell_modal"),
    path('ini_cell_modal/', ini_cell_modal, name="ini_cell_modal"),
    path('ong_cell_modal/content/before_memo/', ong_cell_modal_content_before_memo, name="ong_cell_modal_content_before_memo"),
    path('ong_cell_modal/content/', ong_cell_modal_content, name="ong_cell_modal_content"),
    path('ong_cell_modal/', ong_cell_modal, name="ong_cell_modal"),
    path('cpt_cell_modal/content/after_memo/', cpt_cell_modal_content_after_memo, name="cpt_cell_modal_content_after_memo"),
    path('cpt_cell_modal/content/', cpt_cell_modal_content, name="cpt_cell_modal_content"),
    path('cpt_cell_modal/', cpt_cell_modal, name="cpt_cell_modal"),
    path('mentee/info/', get_mentee_info, name="get_mentee_info"),
    path('chat/body/', get_chat_body, name="get_chat_body"),
]

