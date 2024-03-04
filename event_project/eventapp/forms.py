from django import forms
from .models import Event,Musician, EventOrganizer

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'form_filling_date': forms.DateInput(attrs={'type': 'date'}),
            'event_start_date': forms.DateInput(attrs={'type': 'date'}),
            'event_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MusicianForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = '__all__'

class EventOrganizerForm(forms.ModelForm):
    class Meta:
        model = EventOrganizer
        fields = '__all__'
