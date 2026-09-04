from django import forms
from .models import Build

class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ('game', 'version', 'build_number', 'platform', 'status', 'branch_name', 'git_commit_hash', 'file_size_mb', 'build_duration_sec', 'qa_notes')
        widgets = {
            'qa_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
