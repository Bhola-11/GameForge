from django import forms
from .models import Bug, BugComment

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ('game', 'project', 'title', 'version_found', 'platform', 'severity', 'priority', 'assigned_to', 'steps_to_reproduce', 'expected_result', 'actual_result', 'logs_or_stacktrace')
        widgets = {
            'steps_to_reproduce': forms.Textarea(attrs={'rows': 3, 'placeholder': '1. Launch game on Windows 11\\n2. Open inventory menu...'}),
            'expected_result': forms.Textarea(attrs={'rows': 2}),
            'actual_result': forms.Textarea(attrs={'rows': 2}),
            'logs_or_stacktrace': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Paste callstack or crash log output...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})


class BugCommentForm(forms.ModelForm):
    class Meta:
        model = BugComment
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Triage note or fix verification status...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
