from django.urls import path
from .views import *

app_name = "mentee"

urlpatterns = [
    path('', index , name="index"),
    path('mentor/signup/', mentor_signup, name="mentor_signup"),
    path('mentor/list/', mentor_list, name="mentor_list"),
]

