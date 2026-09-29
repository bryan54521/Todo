import os, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import slots  # noqa: E402

TZ = ZoneInfo("America/New_York")
NOW = datetime(2026, 9, 29, 9, 0, tzinfo=TZ)  # Tuesday


def test_respects_notice_hours_and_weekends():
    s = slots.compute_slots([], NOW, 30, limit=1000)
    assert all(x >= NOW + timedelta(hours=24) for x in s)
    assert all(x.weekday() < 5 for x in s)
    assert all(10 <= x.hour < 16 for x in s)


def test_busy_time_and_buffer_excluded():
    busy_start = datetime(2026, 10, 1, 11, 0, tzinfo=TZ)
    busy = [(busy_start, busy_start + timedelta(hours=1))]
    s = slots.compute_slots(busy, NOW, 30, limit=1000)
    times = {x for x in s if x.date() == busy_start.date()}
    assert datetime(2026, 10, 1, 10, 30, tzinfo=TZ) not in times  # ends inside 15m buffer
    assert datetime(2026, 10, 1, 11, 30, tzinfo=TZ) not in times
    assert datetime(2026, 10, 1, 12, 30, tzinfo=TZ) in times


def test_validator_rejects_bad_slots():
    good = slots.compute_slots([], NOW, 30)[0]
    assert slots.is_slot_valid(good, 30, [], NOW)
    assert not slots.is_slot_valid(good.replace(hour=3), 30, [], NOW)
    assert not slots.is_slot_valid(good, 90, [], NOW)
