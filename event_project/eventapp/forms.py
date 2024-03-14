# forms.py
from django import forms
from .models import Event, Musician, EventOrganizer, UserCredentials

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'created_on': forms.DateInput(attrs={'type': 'date'}),
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

class UserCredentialsForm(forms.ModelForm):
    class Meta:
        model = UserCredentials
        fields = '__all__'
