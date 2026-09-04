from django import forms
from .models import StoreListing

class StoreListingForm(forms.ModelForm):
    class Meta:
        model = StoreListing
        fields = ('game', 'store', 'headline', 'price', 'discount_percentage', 'currency', 'status', 'store_url', 'tags', 'short_description', 'full_description', 'min_cpu', 'min_gpu', 'min_ram_gb', 'min_storage_gb')
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'full_description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'gf-form-control'})
