from django.urls import path
from . import views

urlpatterns = [ # Adiciona a rota para a página inicial
    path('', views.landing_view, name='landing'),
    path('tasks/', views.task_list, name='tasks'),
    path('groups/', views.group_list, name='groups'),
    path('register/', views.register, name='register'), 
    path('user/', views.user, name='user'),
]
