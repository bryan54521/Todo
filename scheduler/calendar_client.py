"""Google Calendar access. Uses an OAuth refresh token supplied via env vars.

Only free/busy is ever exposed to the agent; event details stay private.
"""
import os
import uuid
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import config

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def get_busy(start: datetime, end: datetime):
    body = {"timeMin": start.isoformat(), "timeMax": end.isoformat(), "items": [{"id": "primary"}]}
    resp = _service().freebusy().query(body=body).execute()
    return [
        (datetime.fromisoformat(b["start"]), datetime.fromisoformat(b["end"]))
        for b in resp["calendars"]["primary"]["busy"]
    ]


def create_event(summary, start, end, guest_email, guest_name, description=""):
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start.isoformat(), "timeZone": config.TIMEZONE},
        "end": {"dateTime": end.isoformat(), "timeZone": config.TIMEZONE},
        "attendees": [{"email": guest_email, "displayName": guest_name}],
        "conferenceData": {"createRequest": {"requestId": uuid.uuid4().hex}},
    }
    created = _service().events().insert(
        calendarId="primary", body=event, conferenceDataVersion=1, sendUpdates="all"
    ).execute()
    return created.get("htmlLink"), created.get("hangoutLink")
