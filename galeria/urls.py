from django.urls import path
from django.contrib.auth.views import LogoutView  # Import LogoutView
from . import views

urlpatterns = [
    # Landing page
    path('', views.landing_view, name='landing'),

    # User and Registration Pages
    path('register/', views.register, name='register'), 
    path('user/', views.user, name='user'),

    # Task URLs
    path('tasks/', views.task_list, name='tasks'),
    path('tasks/create/', views.create_task, name='create_task'),

    # Group URLs
    path('groups/', views.group_list, name='groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/join/', views.join_group, name='join_group'),

    # Logout URL with redirection to the landing page after logout
    path('logout/', LogoutView.as_view(next_page='landing'), name='logout'),
]

