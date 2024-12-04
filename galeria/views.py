from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task, StudyGroup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import TaskForm
from django.utils import timezone
import calendar
from datetime import datetime, timedelta

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
    # Obtém a data atual ou a enviada pelo usuário
    current_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))

    try:
        current_date = datetime.strptime(current_date_str, '%Y-%m-%d')
    except ValueError:
        # Fallback para a data atual caso o parâmetro 'date' esteja vazio ou inválido
        current_date = datetime.today().replace(day=1)

    # Verificar mudanças no mês
    change_month = request.GET.get('change_month')
    if change_month == 'previous':
        # Ajustar para o mês anterior
        if current_date.month == 1:  # Janeiro → Dezembro do ano anterior
            current_date = current_date.replace(year=current_date.year - 1, month=12, day=1)
        else:
            current_date = current_date.replace(month=current_date.month - 1, day=1)
    elif change_month == 'next':
        # Ajustar para o próximo mês
        if current_date.month == 12:  # Dezembro → Janeiro do próximo ano
            current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1, day=1)

    # Gerar o calendário para o mês ajustado
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(current_date.year, current_date.month)

    # Nome do mês e ano
    current_month_name = current_date.strftime('%B')
    current_year = current_date.year

    # Obtém a data de hoje no timezone local
    today = timezone.localdate()

    # Filtra as tarefas para hoje
    daily_tasks = Task.objects.filter(user=request.user, due_date=today)

    # Calcula o XP semanal total
    total_weekly_xp = sum(
        DIFFICULTY_XP_MAPPING.get(task.difficulty, 0) for task in Task.objects.filter(user=request.user)
    )

    return render(request, 'user.html', {
        'current_month': current_month_name,
        'current_year': current_year,
        'calendar': month_days,
        'total_weekly_xp': total_weekly_xp,
        'daily_tasks': daily_tasks,
        'current_date': current_date.strftime('%Y-%m-%d'),  # Passar data atual ajustada para o HTML
    })


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
            # Cria o grupo e adiciona o usuário como admin e membro
            group = StudyGroup.objects.create(
                name=group_name,
                description=description,
                admin=request.user,  # Define o criador como admin
                max_members=max_members  # Define o número máximo de membros
            )
            # Adiciona o criador também como membro
            group.members.add(request.user)

            messages.success(request, f"Grupo '{group_name}' criado com sucesso! Você foi adicionado ao grupo.")
            return redirect('groups')  # Redireciona para a lista de grupos

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
