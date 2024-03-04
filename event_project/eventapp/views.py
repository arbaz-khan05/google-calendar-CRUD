from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView , ListView
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import EventSerializer, MusicianSerializer, EventOrganizerSerializer
from .models import Event , Musician, EventOrganizer
from .forms import EventForm ,MusicianForm, EventOrganizerForm
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os.path



class EventListCreate(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class MusicianListCreateAPIView(generics.ListCreateAPIView):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Musician created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MusicianRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Musician created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventOrganizerListCreateAPIView(generics.ListCreateAPIView):
    queryset = EventOrganizer.objects.all()
    serializer_class = EventOrganizerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event Organizer created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventOrganizerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventOrganizer.objects.all()
    serializer_class = EventOrganizerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event Organizer created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html' 
    context_object_name = 'events'  

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        event = form.save()
        service = create_google_service()
        event_id = create_event(service, event)
        event.google_event_id = event_id
        event.save()
        messages.success(self.request, 'Event created successfully.')
        return super().form_valid(form)

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        event = form.save()
        service = create_google_service()
        update_event(service, event.google_event_id, event)
        messages.success(self.request, 'Event updated successfully.')
        return super().form_valid(form)

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        service = create_google_service()
        delete_event(service, event.google_event_id)
        messages.success(request, 'Event deleted successfully.')
        return super().delete(request, *args, **kwargs)


 # Musician Views
class MusicianListView(ListView):
    model = Musician
    template_name = 'musician_list.html'
    context_object_name = 'musicians'

class MusicianCreateView(CreateView):
    model = Musician
    form_class = MusicianForm
    template_name = 'musician_form.html'
    success_url = reverse_lazy('musician_list')

class MusicianUpdateView(UpdateView):
    model = Musician
    form_class = MusicianForm
    template_name = 'musician_form.html'
    success_url = reverse_lazy('musician_list')

class MusicianDeleteView(DeleteView):
    model = Musician
    success_url = reverse_lazy('musician_list')

 # Event Organizer Views
class EventOrganizerListView(ListView):
    model = EventOrganizer
    template_name = 'event_organizer_list.html'
    context_object_name = 'event_organizers'

class EventOrganizerCreateView(CreateView):
    model = EventOrganizer
    form_class = EventOrganizerForm
    template_name = 'event_organizer_form.html'
    success_url = reverse_lazy('event_organizer_list')

class EventOrganizerUpdateView(UpdateView):
    model = EventOrganizer
    form_class = EventOrganizerForm
    template_name = 'event_organizer_form.html'
    success_url = reverse_lazy('event_organizer_list')

class EventOrganizerDeleteView(DeleteView):
    model = EventOrganizer
    success_url = reverse_lazy('event_organizer_list')


