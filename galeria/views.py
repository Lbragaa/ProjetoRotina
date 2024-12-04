from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task, StudyGroup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import TaskForm
from django.utils import timezone

# Difficulty XP Mapping
DIFFICULTY_XP_MAPPING = {
    'easy': 1,
    'medium': 2,
    'hard': 4,
    'veryhard': 6,
}

# Landing Page View
def landing_view(request):
    return render(request, 'landing.html')

# Home Page for Authenticated Users
@login_required
def user(request):
    # Make the comparison with timezone aware settings
    today = timezone.localdate()  # This ensures you get today's date based on the local timezone

    # Debugging print statement to verify dates
    print(f"Todays date: {today}")

    # Filter for today's tasks
    daily_tasks = Task.objects.filter(user=request.user, due_date=today)

    # Calculate total weekly XP by mapping difficulty strings to their respective values
    total_weekly_xp = sum(DIFFICULTY_XP_MAPPING.get(task.difficulty, 0) for task in Task.objects.filter(user=request.user))

    return render(request, 'user.html', {'daily_tasks': daily_tasks, 'total_weekly_xp': total_weekly_xp})

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

# Task List View for Logged-in Users (Tasks for the Week)
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  # Get all tasks related to the logged-in user
    return render(request, 'userPages/tarefas/tasks.html', {'tasks': tasks})

# Create Task View
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associate the task with the logged-in user
            task.save()
            return redirect('tasks')  # Redirect to the tasks list after creation
    else:
        form = TaskForm()
    
    return render(request, 'userPages/tarefas/create_task.html', {'form': form})

# Group List View for Study Groups
@login_required
def group_list(request):
    groups = StudyGroup.objects.all()
    return render(request, 'userPages/gruposDeEstudo/groups.html', {'groups': groups})

# Create Group View
@login_required
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        description = request.POST.get('description')
        max_members = request.POST.get('max_members', 12)

        if group_name:
            # Create the group and associate the user as admin
            group = StudyGroup.objects.create(
                name=group_name,
                description=description,
                admin=request.user,  # Use 'admin' field to associate group with logged-in user
                max_members=max_members  # Set max members
            )
            messages.success(request, f"Grupo '{group_name}' criado com sucesso!")
            return redirect('groups')  # Redirect to the group list
    return render(request, 'userPages/gruposDeEstudo/create_group.html')

# Join Group View
@login_required
def join_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = get_object_or_404(StudyGroup, id=group_id)
        if request.user not in group.members.all():
            group.members.add(request.user)
            messages.success(request, f"Você entrou no grupo '{group.name}'!")
            return redirect('groups')  # Redirect to the group list after joining
    groups = StudyGroup.objects.all()
    return render(request, 'userPages/gruposDeEstudo/join_group.html', {'groups': groups})
