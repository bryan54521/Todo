"""Pure availability logic: turn busy intervals + rules into bookable slots."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import config


def _overlaps(start, end, busy, buffer):
    pad = timedelta(minutes=buffer)
    return any(start < b_end + pad and end > b_start - pad for b_start, b_end in busy)


def compute_slots(busy, now, duration, tz_name=None, limit=None, **rules):
    """Return start datetimes (tz-aware, owner tz) that fit the rules.

    busy: list of (start, end) tz-aware datetimes.
    """
    tz = ZoneInfo(tz_name or config.TIMEZONE)
    work_days = rules.get("work_days", config.WORK_DAYS)
    work_start = rules.get("work_start", config.WORK_START)
    work_end = rules.get("work_end", config.WORK_END)
    step = timedelta(minutes=rules.get("step", config.SLOT_STEP_MINUTES))
    buffer = rules.get("buffer", config.BUFFER_MINUTES)
    earliest = now + timedelta(hours=rules.get("min_notice_hours", config.MIN_NOTICE_HOURS))
    days_ahead = rules.get("max_days_ahead", config.MAX_DAYS_AHEAD)
    limit = limit or config.MAX_SLOTS_RETURNED

    dur = timedelta(minutes=duration)
    out = []
    today = now.astimezone(tz).date()
    for offset in range(days_ahead + 1):
        day = today + timedelta(days=offset)
        if day.weekday() not in work_days:
            continue
        cur = datetime.combine(day, work_start, tz)
        day_end = datetime.combine(day, work_end, tz)
        while cur + dur <= day_end:
            if cur >= earliest and not _overlaps(cur, cur + dur, busy, buffer):
                out.append(cur)
                if len(out) >= limit:
                    return out
            cur += step
    return out


def is_slot_valid(start, duration, busy, now, **rules):
    """Server-side re-check of a slot the model claims is open."""
    if duration not in config.ALLOWED_DURATIONS:
        return False
    day_slots = compute_slots(busy, now, duration, limit=10_000, **rules)
    return any(s == start for s in day_slots)
