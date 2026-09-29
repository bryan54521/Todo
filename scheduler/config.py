import os
from datetime import time

TIMEZONE = os.environ.get("OWNER_TIMEZONE", "America/New_York")
OWNER_NAME = os.environ.get("OWNER_NAME", "the calendar owner")
OWNER_EMAIL = os.environ.get("OWNER_EMAIL", "")
MODEL = os.environ.get("SCHEDULER_MODEL", "claude-sonnet-5-5")

# Availability rules. Edit these to match how you want to be booked.
WORK_DAYS = {0, 1, 2, 3, 4}          # Mon-Fri
WORK_START = time(10, 0)
WORK_END = time(16, 0)
SLOT_STEP_MINUTES = 30
ALLOWED_DURATIONS = (15, 30, 45, 60)
BUFFER_MINUTES = 15                  # gap kept around existing meetings
MIN_NOTICE_HOURS = 24
MAX_DAYS_AHEAD = 21
MAX_SLOTS_RETURNED = 12

# Abuse protection for the public endpoint.
MAX_MESSAGE_CHARS = 1000
MAX_TURNS = 20
RATE_LIMIT_PER_HOUR = 30             # chat requests per IP
MAX_PENDING_PER_EMAIL = 2

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
NOTIFY_WEBHOOK_URL = os.environ.get("NOTIFY_WEBHOOK_URL", "")  # Slack-compatible
