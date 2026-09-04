from django import forms
from .models import Leaderboard

class LeaderboardForm(forms.ModelForm):
    class Meta:
        model = Leaderboard
        fields = ('game', 'name', 'metric_type', 'sort_order', 'season_name', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'gf-form-control'})
