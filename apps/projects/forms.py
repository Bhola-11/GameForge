from django import forms
from .models import Project, ProjectMember, ProjectRisk

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('organization', 'game', 'title', 'lead', 'status', 'priority', 'start_date', 'end_date', 'budget', 'progress_percentage', 'description')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
