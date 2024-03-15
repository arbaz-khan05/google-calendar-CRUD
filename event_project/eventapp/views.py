from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import EventSerializer, MusicianSerializer, EventOrganizerSerializer, UserCredentialsSerializer, EventNameSerializer
from .models import Event, Musician, EventOrganizer, UserCredentials
from rest_framework.views import APIView
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
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

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# Musician views
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


# Event Organizer Views
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

#Login Views
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

# Filter By email Views
class EventFilterByEmailAPIView(generics.ListAPIView):
    serializer_class = EventNameSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        return Event.objects.filter(event_organiser_email=email)
