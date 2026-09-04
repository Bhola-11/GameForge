from django import forms
from .models import InGameItem

class InGameItemForm(forms.ModelForm):
    class Meta:
        model = InGameItem
        fields = ('game', 'name', 'sku', 'item_type', 'price', 'currency', 'is_active', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'gf-form-control'})
