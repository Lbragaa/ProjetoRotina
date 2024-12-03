from django.urls import path
from . import views

urlpatterns = [ # Adiciona a rota para a página inicial
    path('', views.landing_view, name='landing'),
    path('tasks/', views.task_list, name='tasks'),
    path('register/', views.register, name='register'), 
    path('user/', views.user, name='user'),

    #grupo de estudo
    path('groups/', views.group_list, name='groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/join/', views.join_group, name='join_group'),
]
