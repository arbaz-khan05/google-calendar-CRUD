from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'form_filling_date': forms.DateInput(attrs={'type': 'date'}),
            'event_start_date': forms.DateInput(attrs={'type': 'date'}),
            'event_end_date': forms.DateInput(attrs={'type': 'date'}),
        }
