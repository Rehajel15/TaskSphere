from django import forms
from home.models import Table_task
from authentication.models import User

class CreateTaskForm(forms.ModelForm):
    task_name = forms.CharField(
        label="Taskname", 
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Title of the task',
        }),
    )
    task_description = forms.CharField(
        label="Task description",
        max_length=250,
        required=False, 
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Description of the task', 
            'rows': '4',
        }),
    )
    current_column = forms.ChoiceField(
        choices=[('ToDo', 'ToDo'), ('In progress', 'In progress'), ('Done', 'Done')],
        widget=forms.Select(attrs={
            'class': 'form-select bg-secondary text-white'
        }),
    )
    current_worker = forms.ChoiceField(
        choices=[],  # Wird dynamisch im __init__ gesetzt
        widget=forms.Select(attrs={
            'class': 'form-select bg-secondary text-white'
        }),
        required=True,
        label="Current worker"
    )
    deadLine = forms.DateTimeField(
        label="Deadline",
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control bg-secondary text-white'
            }
        )
    )

    class Meta:
        model = Table_task
        fields = '__all__'

    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        if group:
            users = group.users.all()
            self.fields['current_worker'].choices = [
                (f"{user.firstname} {user.lastname}") for user in users
            ]