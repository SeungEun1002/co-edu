from django.shortcuts import render, redirect
from user.models import *
from .forms import *
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'mentee/layout.html')

@login_required
def mentor_signup(request):
    if request.method == 'POST':
        form = MentorSignupForm(request.POST)

        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.user = request.user
            mentor.save()
            form.save_m2m()

            #is_mentor 수정
            user=request.user
            user.is_mentor=True
            user.save()

            return redirect('mentor:index')
    else:
        form = MentorSignupForm()
    return render(request, 'mentee/mentor_signup.html', {'form': form})

@login_required
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