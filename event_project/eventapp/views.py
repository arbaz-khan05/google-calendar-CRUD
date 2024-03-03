from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Event
from .forms import EventForm
from rest_framework import generics
from .serializers import EventSerializer
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os.path

class EventListCreate(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'eventapp/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_google_service():
    creds = authenticate()
    return build('calendar', 'v3', credentials=creds)

def create_event(service, event):
    event_data = {
        'summary': event.event_name,
        'location': event.location,
        'description': event.description,
        'start': {'dateTime': event.event_start_date.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': event.event_end_date.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'attendees': [{'email': email} for email in event.attendees_gmail.split(',')]
    }
    created_event = service.events().insert(calendarId='primary', body=event_data).execute()
    event_id = created_event['id']
    return event_id

def update_event(service, event_id, event):
    event_data = {
        'summary': event.event_name,
        'location': event.location,
        'description': event.description,
        'start': {'dateTime': event.event_start_date.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': event.event_end_date.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'attendees': [{'email': email} for email in event.attendees_gmail.split(',')]
    }
    service.events().update(calendarId='primary', eventId=event_id, body=event_data).execute()

def delete_event(service, event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            service = create_google_service()
            event_id = create_event(service, event)
            event.google_event_id = event_id
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            service = create_google_service()
            update_event(service, event.google_event_id, event)
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    service = create_google_service()
    delete_event(service, event.google_event_id)
    event.delete()
    return redirect('event_list')
