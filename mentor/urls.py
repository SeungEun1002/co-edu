from django.urls import path
from .views import *

app_name = "mentor"

urlpatterns = [
    path('', index , name="index"),
    path('list/', mentor_list, name="mentor_list"),
]

