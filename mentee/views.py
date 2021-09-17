from django.shortcuts import render
from user.models import *

def index(request):
    return render(request, 'mentee/layout.html')

def mentor_list(request):
    qs = Mentor.objects.all()[:4]   # TODO: Paging
    mentor_list = list()
    for i in range(2):
        inner_list = list()
        for j in range (2):
            inner_list.append(qs[2*i+j])
        mentor_list.append(inner_list)

    context = {
        'mentor_list': mentor_list
    }
    return render(request, 'mentee/mentor_list.html', context)