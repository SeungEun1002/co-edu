from django.urls import path
from .views import *

app_name = "mentee"

urlpatterns = [
    path('', index , name="index"),
    path('info/', mentee_info, name="mentee_info"),
    path('mentor/signup/', mentor_signup, name="mentor_signup"),
    path('mentor/list/', mentor_list, name="mentor_list"),
    path('mentoring/application', mentoring_application, name="mentoring_application"),
    path('timetable/', mentee_timetable, name="mentee_timetable"),
    path('requestong_cell_modal/content/', requestong_cell_modal_content, name="requestong_cell_modal_content"),
    path('requestong_cell_modal/', requestong_cell_modal, name="requestong_cell_modal"),
    path('mentoringong_cell_modal/content/', mentoringong_cell_modal_content, name="mentoringong_cell_modal_content"),
    path('mentoringong_cell_modal/', mentoringong_cell_modal, name="mentoringong_cell_modal"),
    path('cpt_cell_modal/content/', cpt_cell_modal_content, name="cpt_cell_modal_content"),
    path('cpt_cell_modal/', cpt_cell_modal, name="cpt_cell_modal"),

]

