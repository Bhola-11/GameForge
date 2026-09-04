from django import forms
from .models import Task, TaskComment, TaskTimeLog

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('project', 'title', 'task_type', 'status', 'priority', 'assigned_to', 'due_date', 'estimated_hours', 'description')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write an engineering or design update...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})


class TaskTimeLogForm(forms.ModelForm):
    class Meta:
        model = TaskTimeLog
        fields = ('hours', 'date', 'description')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
