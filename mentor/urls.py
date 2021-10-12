from django.urls import path
from .views import *

app_name = "mentor"

urlpatterns = [
    path('', index , name="index"),
    path('info/', mentor_info, name="mentor_info"),
    path('mentoring/', mentoring_list , name="mentoring_list"),
    path('timetable/', mentor_timetable, name="mentor_timetable"),
    path('empty_cell_modal/', empty_cell_modal, name="empty_cell_modal"),
    path('available_cell_modal/', available_cell_modal, name="available_cell_modal"),
]

