from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task, StudyGroup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def minha_view(request):
    # Código da view que exige autenticação
    pass


def home(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Conta criada com sucesso para {username}!")
            return redirect('login')  # Redireciona para a página de login após o registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user(request):
    return render(request, 'user.html')

def task_list(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    else:
        tasks = Task.objects.none()  # Retorna uma lista vazia se não estiver autenticado
    return render(request, 'tasks.html', {'tasks': tasks})

def group_list(request):
    groups = StudyGroup.objects.all()
    return render(request, 'groups.html', {'groups': groups})
