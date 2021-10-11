from django.urls import path
from .views import *

app_name = "mentee"

urlpatterns = [
    path('', index , name="index"),
    path('info/', mentee_info, name="mentee_info"),
    path('mentor/signup/', mentor_signup, name="mentor_signup"),
    path('mentor/list/', mentor_list, name="mentor_list"),
    path('mentoring/application', mentoring_application, name="mentoring_application"),
]

