from django import forms
from .models import Achievement

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ('game', 'code', 'name', 'tier', 'points', 'icon_name', 'is_hidden', 'is_active', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'gf-form-control'})
