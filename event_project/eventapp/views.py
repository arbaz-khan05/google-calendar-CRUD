from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import EventSerializer, MusicianSerializer, EventOrganizerSerializer, UserCredentialsSerializer
from .models import Event, Musician, EventOrganizer, UserCredentials
from .forms import EventForm, MusicianForm, EventOrganizerForm
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rest_framework.views import APIView
import pickle
import os.path
import uuid

# Event Views

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Error loading credentials: {e}")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('eventapp/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error running local server: {e}")
            else:
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
    return creds

def create_google_service():
    creds = authenticate()
    return build('calendar', 'v3', credentials=creds)

def generate_unique_google_event_id():
    return str(uuid.uuid4())

def create_event(service, event):
    event_data = {
        'summary': event.event_name,
        'location': event.location,
        'description': event.description,
        'start': {'dateTime': event.event_start_date.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': event.event_end_date.isoformat(), 'timeZone': 'Asia/Kolkata'},
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
    }
    service.events().update(calendarId='primary', eventId=event_id, body=event_data).execute()

def delete_event(service, event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()

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
        event = form.save(commit=False)
        # Check if the generated google_event_id already exists
        while True:
            google_event_id = generate_unique_google_event_id()
            if not Event.objects.filter(google_event_id=google_event_id).exists():
                event.google_event_id = google_event_id
                break
        event.save()
        # Create event in Google Calendar
        service = create_google_service()
        create_event(service, event)
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
    template_name = 'event_delete.html'
    success_url = reverse_lazy('event_list')

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        service = create_google_service()
        delete_event(service, event.google_event_id)
        messages.success(request, 'Event deleted successfully.')
        return super().delete(request, *args, **kwargs)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        events = self.get_queryset()
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(event)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


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
    template_name = 'musician_delete.html'
    success_url = reverse_lazy('musician_list')

class MusicianList(generics.ListAPIView):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer

class MusicianListCreateAPIView(generics.ListCreateAPIView):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user_credential = UserCredentials.objects.get(email=email)
                if user_credential.category == 'musician':
                    serializer.save()
                    return Response({"message": "Musician created successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Incorrect category"}, status=status.HTTP_400_BAD_REQUEST)
            except UserCredentials.DoesNotExist:
                return Response({"error": "Email not found in User Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MusicianRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer

    def get(self, request, *args, **kwargs):
        musician = self.get_object()
        serializer = self.get_serializer(musician)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Musician created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    template_name = 'event_organizer_delete.html'
    success_url = reverse_lazy('event_organizer_list')

class EventOrganizerList(generics.ListAPIView):
    queryset = EventOrganizer.objects.all()
    serializer_class = EventOrganizerSerializer

class EventOrganizerListCreateAPIView(generics.ListCreateAPIView):
    queryset = EventOrganizer.objects.all()
    serializer_class = EventOrganizerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user_credential = UserCredentials.objects.get(email=email)
                if user_credential.category == 'event organizer':
                    serializer.save()
                    return Response({"message": "Event Organizer created successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Incorrect category"}, status=status.HTTP_400_BAD_REQUEST)
            except UserCredentials.DoesNotExist:
                return Response({"error": "Email not found in User Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventOrganizerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventOrganizer.objects.all()
    serializer_class = EventOrganizerSerializer

    def get(self, request, *args, **kwargs):
        event_organizer = self.get_object()
        serializer = self.get_serializer(event_organizer)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event Organizer created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Credentials Views
class UserCredentialsCreateView(generics.CreateAPIView):
    serializer_class = UserCredentialsSerializer

    def create(self, request, *args, **kwargs):
        # Get the email from the request data
        email = request.data.get('email')

        # Check if email already exists
        if UserCredentials.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists. Please Login'}, status=status.HTTP_400_BAD_REQUEST)

        user_credentials_serializer = self.get_serializer(data=request.data)
        if user_credentials_serializer.is_valid():
            user_credentials_serializer.save()
            return Response({'user_credentials': user_credentials_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(user_credentials_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API Views

class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_credentials = UserCredentials.objects.get(email=email)
            if user_credentials.password == password:
                # Password matches, authentication successful
                if user_credentials.category == 'musician':
                    try:
                        musician = Musician.objects.get(email=email)
                        serializer = MusicianSerializer(musician)
                        return Response({
                            'memberType': 'musician',
                            'details': serializer.data
                        }, status=status.HTTP_200_OK)
                    except Musician.DoesNotExist:
                        return Response({'error': 'Musician not found'}, status=status.HTTP_404_NOT_FOUND)
                elif user_credentials.category == 'event_organizer':
                    try:
                        event_organizer = EventOrganizer.objects.get(email=email)
                        serializer = EventOrganizerSerializer(event_organizer)
                        return Response({
                            'memberType': 'event organizer',
                            'details': serializer.data
                        }, status=status.HTTP_200_OK)
                    except EventOrganizer.DoesNotExist:
                        return Response({'error': 'Event Organizer not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Password doesn't match
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except UserCredentials.DoesNotExist:
            # User not found
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
