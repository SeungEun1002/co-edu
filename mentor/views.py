from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'mentor/layout.html')

def mentor_list(request):
    return render(request, 'mentor/mentor_list.html')