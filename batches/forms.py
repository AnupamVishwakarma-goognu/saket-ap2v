from django import forms
from .models import (
    Batches
)

class BatchesUpdateViewModelForm(forms.ModelForm):
    class Meta:
        model = Batches
        exclude = ('batch_name', 'end_time',
                'duration', 'create_on', 'courses')
