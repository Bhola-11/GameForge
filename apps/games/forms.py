from django import forms
from .models import Game, GameMilestone

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('organization', 'title', 'genre', 'engine', 'platforms', 'status', 'target_release_date', 'budget', 'repository_url', 'summary', 'description')
        widgets = {
            'target_release_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'summary': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
