from django import forms
from .models import Organization, Department, OrgMember, OrgInvitation

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'description', 'website', 'plan_tier', 'logo')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'gf-form-control'})


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'code', 'lead', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})


class OrgInvitationForm(forms.ModelForm):
    class Meta:
        model = OrgInvitation
        fields = ('email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
