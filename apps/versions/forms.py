from django import forms
from .models import GameVersion

class GameVersionForm(forms.ModelForm):
    class Meta:
        model = GameVersion
        fields = ('game', 'version_number', 'release_type', 'status', 'release_date', 'changelog')
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'changelog': forms.Textarea(attrs={'rows': 4, 'placeholder': '- Added new boss encounter\\n- Optimized ray tracing shaders\\n- Fixed audio desync in multiplayer'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
