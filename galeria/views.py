from django.shortcuts import render, redirect, get_object_or_404
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
    return render(request, 'userPages/gruposDeEstudo/groups.html', {'groups': groups})

# Create Group View
@login_required
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        description = request.POST.get('description')
        max_members = request.POST.get('max_members', 12)

        if group_name:
            # Cria o grupo e associa o usuário como admin
            group = StudyGroup.objects.create(
                name=group_name,
                description=description,
                admin=request.user,  # Usa o campo 'admin' para associar o grupo ao usuário logado
                max_members=max_members  # Define o máximo de membros
            )
            messages.success(request, f"Grupo '{group_name}' criado com sucesso!")
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
