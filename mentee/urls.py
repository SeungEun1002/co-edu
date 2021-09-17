from django.urls import path
from .views import *

app_name = "mentee"

urlpatterns = [
    path('', index , name="index"),
    path('mentor/list/', mentor_list, name="mentor_list"),
]

