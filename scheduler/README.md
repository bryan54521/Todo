# Meeting scheduling agent

A public chat page where visitors request time on your Google Calendar. A Claude agent finds open slots and files a request; **you approve each one** on a private admin page before it lands on your calendar.

## Safety model (external visitors)
- The agent only sees free/busy-derived slots, never event titles or attendees.
- It has two tools: `get_available_slots` and `submit_meeting_request` (which does not book).
- Submitted slots are re-validated server-side against the calendar and your rules, and again on approval.
- Rate limit per IP, message/turn caps, pending-request cap per email.
- `/admin` returns 404 unless `ADMIN_TOKEN` matches.

## Configure
Edit `config.py` for hours, durations, buffers and notice. Environment variables:

| Var | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` | OAuth for your calendar (scope `calendar`) |
| `OWNER_NAME`, `OWNER_EMAIL`, `OWNER_TIMEZONE` | Display and timezone (IANA) |
| `ADMIN_TOKEN` | Long random string for `/admin?token=...` |
| `NOTIFY_WEBHOOK_URL` | Optional Slack-compatible webhook pinged on new requests |

## Run
    pip install -r requirements.txt
    python -m pytest tests
    gunicorn app:app

Serve over HTTPS. The SQLite file is fine for one instance; use a real DB if you scale out (the rate limiter is also in-memory).
