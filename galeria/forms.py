from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'due_date', 'due_time', 'difficulty']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.TextInput(attrs={'placeholder': 'Descrição da tarefa'}),
            'difficulty': forms.Select(),  # Choices are already defined in the model, so no changes needed here.
        }
