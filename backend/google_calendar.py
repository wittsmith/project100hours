import os
import json
import boto3
import tempfile
import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# AWS SSM Client
ssm = boto3.client("ssm", region_name="us-east-1")

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_ssm_parameter(param_name, with_decryption=True):
    """Retrieve a secure parameter from AWS SSM Parameter Store."""
    try:
        response = ssm.get_parameter(Name=param_name, WithDecryption=with_decryption)
        return response["Parameter"]["Value"]
    except Exception as e:
        print(f"❌ Error fetching SSM parameter {param_name}: {e}")
        return None

def get_google_credentials():
    """Retrieve Google API credentials from AWS SSM and load them correctly."""
    try:
        credentials_json = get_ssm_parameter("GOOGLE_CREDENTIALS")
        if not credentials_json:
            raise Exception("❌ Missing Google API credentials in SSM!")

        # Write credentials to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as temp_cred_file:
            temp_cred_file.write(credentials_json)
            temp_cred_file_path = temp_cred_file.name

        # Load credentials from temp file
        credentials = Credentials.from_service_account_file(temp_cred_file_path, scopes=SCOPES)

        print("✅ Successfully loaded Google API credentials.")
        return credentials

    except Exception as e:
        print(f"❌ Google Credentials Error: {e}")
        return None

def get_weekly_events(start_date=None, end_date=None):
    """Fetches weekly events from Google Calendar."""
    creds = get_google_credentials()
    if not creds:
        return {"error": "Failed to load Google credentials"}

    try:
        service = build("calendar", "v3", credentials=creds)

        # Determine date range
        if start_date and end_date:
            time_min = f"{start_date}T00:00:00Z"
            time_max = f"{end_date}T23:59:59Z"
        else:
            now = datetime.datetime.utcnow()
            start_of_week = now - datetime.timedelta(days=now.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=7)
            time_min = f"{start_of_week.isoformat()}Z"
            time_max = f"{end_of_week.isoformat()}Z"

        print(f"📅 Fetching events from {time_min} to {time_max}")

        # Fetch events
        events_result = service.events().list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        if not events:
            print("ℹ️ No upcoming events found.")

        # Extract relevant details
        simplified_events = []
        for event in events:
            title = event.get("summary", "No Title")
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))

            meet_link = None
            if "conferenceData" in event:
                entry_points = event["conferenceData"].get("entryPoints", [])
                for entry in entry_points:
                    if entry.get("entryPointType") == "video":
                        meet_link = entry.get("uri")

            simplified_events.append({
                "title": title,
                "start": start,
                "end": end,
                "meet_link": meet_link
            })

        print(f"✅ Successfully fetched {len(simplified_events)} events.")
        return simplified_events

    except Exception as e:
        print(f"❌ Google Calendar API Error: {e}")
        return {"error": str(e)}

def create_calendar_event(summary, start_time, end_time, description=""):
    """Creates an event in Google Calendar."""
    creds = get_google_credentials()
    if not creds:
        return {"error": "Failed to load Google credentials"}

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": "America/New_York"},
            "end": {"dateTime": end_time, "timeZone": "America/New_York"},
        }

        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"✅ Created event: {event['htmlLink']}")
        return event["htmlLink"]

    except Exception as e:
        print(f"❌ Google Calendar Event Creation Error: {e}")
        return {"error": str(e)}
