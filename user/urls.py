from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('login/', signin, name="login"),
    path('signup/', signup, name="signup"),
    path('subject/', subject, name="subject"),
]

