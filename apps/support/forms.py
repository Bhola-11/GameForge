from django import forms
from .models import SupportTicket, TicketMessage

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ('player', 'subject', 'category', 'priority', 'status', 'assigned_agent', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})


class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type official support agent response to player...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
