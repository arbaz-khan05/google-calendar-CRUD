from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_id', 'event_name', 'description', 'date', 'organiser_email', 'organiser_name']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  
        }