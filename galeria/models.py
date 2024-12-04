from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()  # Date only for due date
    due_time = models.TimeField(default="00:00")  # Added time field for scheduling
    difficulty = models.IntegerField(choices=[
        (1, 'Fácil (10 a 30 min)'),
        (2, 'Médio (30 min a 1h30)'),
        (4, 'Difícil (1h30 a 3h)'),
        (6, 'Muito Difícil (Acima de 3h)'),
    ])  # Changed to IntegerField with numeric choices for easier calculations
    status = models.BooleanField(default=False)  # Indicates if the task is completed or not
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_groups")
    members = models.ManyToManyField(User, related_name="study_groups")
    max_members = models.IntegerField(default=12)  # Added max_members to match the view

    def __str__(self):
        return self.name
