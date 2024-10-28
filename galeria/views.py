from django.shortcuts import render
from django.http import HttpResponse
from .models import Task, StudyGroup

def index(request):
    return HttpResponse('<h1>OrderlyMind</h1>')

def task_list(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    else:
        tasks = Task.objects.none()  # Retorna uma lista vazia se não estiver autenticado
    return render(request, 'galeria/task_list.html', {'tasks': tasks})

def group_list(request):
    groups = StudyGroup.objects.all()
    return render(request, 'galeria/group_list.html', {'groups': groups})
