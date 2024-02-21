from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os.path

# Define the scopes needed for the Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    creds = None

    # Check if there is already a token.pickle file with credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_event(service):
    event = {
        'summary': 'Example Event',
        'location': 'India',
        'description': 'This is sample description',
        'start': {'dateTime': '2024-02-23T09:00:00', 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': '2024-02-23T10:00:00', 'timeZone': 'Asia/Kolkata'},
    }

    # Create the event
    created_event = service.events().insert(calendarId='primary', body=event).execute()

    # Extract the event ID from the created event
    event_id = created_event['id']
    
    return event_id

def update_event(service, event_id, summary=None, location=None, description=None, start_time=None, end_time=None):
    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    if summary:
        event['summary'] = summary
    if location:
        event['location'] = location
    if description:
        event['description'] = description
    if start_time:
        event['start']['dateTime'] = start_time
    if end_time:
        event['end']['dateTime'] = end_time

    try:
        updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
        print('Event updated: %s' % (updated_event.get('htmlLink')))
    except Exception as e:
        print('Error updating event:', e)

def cancel_event(service, event_id):
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print('Event canceled successfully.')
    except Exception as e:
        print('Error canceling event:', e)

def delete_event(service, event_id):
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print('Event deleted successfully.')
    except Exception as e:
        print('Error deleting event:', e)

if __name__ == '__main__':
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)

    # Example usage:
    event_id = create_event(service)
    print('Event ID:', event_id)

    # Updating Event
    update_event(service, f'{event_id}', summary='Updated Meeting')
    # Cancel Event
    # cancel_event(service, f'{event_id}')
    # Delete Event
    # delete_event(service, f'{event_id}')
    # delete_event(service, 'ngcct4ruqcs11jl4mmknq3md8s')
