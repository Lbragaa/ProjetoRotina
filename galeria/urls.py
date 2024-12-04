from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path('', views.landing_view, name='landing'),

    # User and Registration Pages
    path('register/', views.register, name='register'), 
    path('user/', views.user, name='user'),

    # Task URLs
    path('tasks/', views.task_list, name='tasks'),
    path('tasks/create/', views.create_task, name='create_task'),  # New route for creating a task

    # Group URLs
    path('groups/', views.group_list, name='groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/join/', views.join_group, name='join_group'),
]
