from django import forms
from .models import Release, ReleaseChecklist

class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        fields = ('game', 'version', 'build', 'release_code', 'title', 'target_platform', 'status', 'scheduled_date', 'release_notes')
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'release_notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
