import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import datetime
import boto3
import io

ssm = boto3.client("ssm", region_name="us-east-1")  
# Load environment variables




SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_credentials():
    """Retrieve Google API credentials via OAuth 2.0 instead of a service account."""
    creds = None
    token_path = "token.json"

    # Check if a token already exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        print("🔑 No valid credentials found. Starting OAuth login...")
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials for next time
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds


def get_weekly_events(start_date=None, end_date=None):
    """Fetches weekly events from Google Calendar."""
    creds = get_google_credentials()

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Determine date range
        if start_date and end_date:
            time_min = datetime.datetime.strptime(start_date, "%Y-%m-%d").isoformat() + 'Z'
            time_max = datetime.datetime.strptime(end_date, "%Y-%m-%d").isoformat() + 'Z'
        else:
            now = datetime.datetime.utcnow()
            start_of_week = now - datetime.timedelta(days=now.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=7)
            time_min = start_of_week.isoformat() + 'Z'
            time_max = end_of_week.isoformat() + 'Z'

        # Fetch events
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        # Extract relevant details
        simplified_events = []
        for event in events:
            title = event.get('summary', 'No Title')
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            meet_link = None
            if 'conferenceData' in event:
                entry_points = event['conferenceData'].get('entryPoints', [])
                for entry in entry_points:
                    if entry.get('entryPointType') == 'video':
                        meet_link = entry.get('uri')

            simplified_events.append({
                'title': title,
                'start': start,
                'end': end,
                'meet_link': meet_link
            })

        return simplified_events

    except Exception as e:
        raise Exception(f"Google Calendar API Error: {str(e)}")
    
def create_calendar_event(summary, start_time, end_time, description=""):
    """Creates an event in Google Calendar."""
    creds = get_google_credentials()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "America/New_York"},
        "end": {"dateTime": end_time, "timeZone": "America/New_York"},
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    return event["htmlLink"]  # Returns the calendar event link
