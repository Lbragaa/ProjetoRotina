from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Adiciona a rota para a página inicial
    path('tasks/', views.task_list, name='task_list'),
    path('groups/', views.group_list, name='group_list'),
]
