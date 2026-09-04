"""Weather blueprint backed by the Google Maps Platform Weather API.

The Weather API (weather.googleapis.com) is the developer-facing product
built on Google DeepMind's WeatherNext forecasting models:
https://developers.google.com/weathernext/guides/models

Requires a Google Cloud API key with the Weather API and Geocoding API
enabled, supplied via the GOOGLE_MAPS_API_KEY environment variable.
"""

import os
from datetime import date, datetime

import requests
from flask import Blueprint, render_template, request

weather_bp = Blueprint("weather", __name__)

WEATHER_BASE = "https://weather.googleapis.com/v1"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
REQUEST_TIMEOUT = 10


def _api_key():
    return os.environ.get("GOOGLE_MAPS_API_KEY") or os.environ.get(
        "GOOGLE_WEATHER_API_KEY"
    )


def geocode_city(query, key):
    """Resolve a free-text place name to (lat, lng, formatted address)."""
    resp = requests.get(
        GEOCODE_URL,
        params={"address": query, "key": key},
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "OK" or not data.get("results"):
        raise LookupError(
            f"Could not find a location for '{query}' "
            f"(geocoder status: {data.get('status', 'UNKNOWN')})"
        )
    result = data["results"][0]
    loc = result["geometry"]["location"]
    return loc["lat"], loc["lng"], result.get("formatted_address", query)


def _weather_get(endpoint, key, lat, lng, units, extra=None):
    params = {
        "key": key,
        "location.latitude": lat,
        "location.longitude": lng,
        "unitsSystem": units,
    }
    if extra:
        params.update(extra)
    resp = requests.get(
        f"{WEATHER_BASE}/{endpoint}", params=params, timeout=REQUEST_TIMEOUT
    )
    if resp.status_code != 200:
        try:
            message = resp.json()["error"]["message"]
        except Exception:
            message = resp.text[:200]
        raise RuntimeError(f"Weather API error ({resp.status_code}): {message}")
    return resp.json()


def _degrees(measure):
    if isinstance(measure, dict) and measure.get("degrees") is not None:
        return round(measure["degrees"])
    return None


def _condition(node):
    cond = (node or {}).get("weatherCondition", {})
    icon_base = cond.get("iconBaseUri")
    return {
        "text": cond.get("description", {}).get("text", ""),
        "icon": f"{icon_base}.svg" if icon_base else None,
    }


def _precip_percent(node):
    return (
        (node or {})
        .get("precipitation", {})
        .get("probability", {})
        .get("percent")
    )


def fetch_current(key, lat, lng, units):
    data = _weather_get("currentConditions:lookup", key, lat, lng, units)
    wind = data.get("wind", {})
    return {
        **_condition(data),
        "temp": _degrees(data.get("temperature")),
        "feels_like": _degrees(data.get("feelsLikeTemperature")),
        "humidity": data.get("relativeHumidity"),
        "uv_index": data.get("uvIndex"),
        "cloud_cover": data.get("cloudCover"),
        "precip_percent": _precip_percent(data),
        "wind_speed": wind.get("speed", {}).get("value"),
        "wind_unit": wind.get("speed", {}).get("unit", "").replace("_", " ").lower(),
        "wind_dir": wind.get("direction", {}).get("cardinal", "").replace("_", "-").title(),
        "is_daytime": data.get("isDaytime", True),
    }


def fetch_hourly(key, lat, lng, units, hours=24):
    data = _weather_get(
        "forecast/hours:lookup", key, lat, lng, units, extra={"hours": hours}
    )
    out = []
    for hour in data.get("forecastHours", []):
        dt = hour.get("displayDateTime", {})
        out.append(
            {
                **_condition(hour),
                "label": f"{dt.get('hours', 0):02d}:00",
                "temp": _degrees(hour.get("temperature")),
                "precip_percent": _precip_percent(hour),
            }
        )
    return out


def fetch_daily(key, lat, lng, units, days=10):
    data = _weather_get(
        "forecast/days:lookup", key, lat, lng, units, extra={"days": days}
    )
    out = []
    for day in data.get("forecastDays", []):
        d = day.get("displayDate", {})
        try:
            day_date = date(d["year"], d["month"], d["day"])
            day_name = day_date.strftime("%a")
            date_label = day_date.strftime("%b %-d")
        except (KeyError, ValueError):
            day_name, date_label = "", ""
        sun = day.get("sunEvents", {})
        out.append(
            {
                **_condition(day.get("daytimeForecast")),
                "day_name": day_name,
                "date_label": date_label,
                "max": _degrees(day.get("maxTemperature")),
                "min": _degrees(day.get("minTemperature")),
                "precip_percent": _precip_percent(day.get("daytimeForecast")),
                "sunrise": _format_time(sun.get("sunriseTime")),
                "sunset": _format_time(sun.get("sunsetTime")),
            }
        )
    return out


def _format_time(iso_string):
    if not iso_string:
        return None
    try:
        return datetime.fromisoformat(iso_string.replace("Z", "+00:00")).strftime(
            "%H:%M"
        )
    except ValueError:
        return None


@weather_bp.route("/weather")
def weather():
    key = _api_key()
    query = request.args.get("q", "").strip()
    units = request.args.get("units", "METRIC")
    if units not in ("METRIC", "IMPERIAL"):
        units = "METRIC"

    context = {
        "query": query,
        "units": units,
        "deg_unit": "°F" if units == "IMPERIAL" else "°C",
        "api_key_missing": not key,
        "error": None,
        "place": None,
        "current": None,
        "hourly": [],
        "daily": [],
    }

    if key and query:
        try:
            lat, lng, place = geocode_city(query, key)
            context["place"] = place
            context["current"] = fetch_current(key, lat, lng, units)
            context["hourly"] = fetch_hourly(key, lat, lng, units)
            context["daily"] = fetch_daily(key, lat, lng, units)
        except (requests.RequestException, LookupError, RuntimeError) as exc:
            context["error"] = str(exc)

    return render_template("weather.html", **context)
