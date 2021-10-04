from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
from .forms import *

def home(request):
    logout(request)
    print(request.user)
    return render(request, 'user/home.html')

def signin(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            submit_btn = request.POST.get('submit_btn')
            if submit_btn == '멘토로 로그인':
                return redirect('mentor:index')
            else:
                return redirect('mentee:index')

    else:
        pass
    return render(request, 'user/login.html')

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('mentee:index')
    else:
        form=SignUpForm()
    return render(request, 'user/signup.html', {'form':form})

def subject(request):
    # 1. GET요청과 POST요청 구분
    if request.method == 'POST':
        # POST 요청
        # 2. POST 요청 - 전달된 데이터를 추출
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        # 2.5. 전달된 데이터의 유효성 검사

        # 3. 데이터를 DB에 저장
    else:
        # GET 요청
        form = SubjectForm()
    return render(request, 'user/subject.html', {'form':form})
