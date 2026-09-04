from django import forms
from .models import Team, TeamMember

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('organization', 'name', 'lead', 'description', 'color_code')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'color_code': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ('user', 'role_in_team', 'allocation_percentage')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
