from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task, StudyGroup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Landing Page View
def landing_view(request):
    return render(request, 'landing.html')


# Home Page for Authenticated Users
@login_required
def user(request):
    return render(request, 'user.html')


# Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Conta criada com sucesso para {username}!")
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Task List View for Logged-in Users
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'userPages/tasks.html', {'tasks': tasks})


# Group List View for Study Groups
@login_required
def group_list(request):
    groups = StudyGroup.objects.all()
    return render(request, 'userPages/groups.html', {'groups': groups})
