from django.urls import path
from .views import *

app_name = "mentor"

urlpatterns = [
    path('', index , name="index"),
    path('mentoring/', mentoring_list , name="mentoring_list"),
]

