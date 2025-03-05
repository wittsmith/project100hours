import os
import json
import datetime
import boto3
import io
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# AWS SSM Client
ssm = boto3.client("ssm", region_name="us-east-1")

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
    """Fetches weekly events from Google Calendar using OAuth 2.0."""
    creds = get_google_credentials()
    
    if not creds:
        return {"error": "Failed to authenticate with Google"}

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
