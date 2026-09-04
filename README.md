# To-Do + Weather

A small Flask app with two pages:

- `/` — the original to-do list (SQLite via Flask-SQLAlchemy)
- `/weather` — a weather app built on Google's weather stack

## How the weather app relates to WeatherNext

[WeatherNext](https://developers.google.com/weathernext/guides/models) is
Google DeepMind's family of AI forecasting models. The raw model outputs are
distributed through BigQuery, Earth Engine, and Vertex AI — all behind an
access-request/early-access program, and as gridded scientific data rather
than a ready-to-use forecast endpoint.

For applications, Google exposes those forecasts through the
[Google Maps Platform Weather API](https://developers.google.com/maps/documentation/weather)
(`weather.googleapis.com`), which is enhanced with the WeatherNext neural
models and only needs an API key. This app uses that API:

| Endpoint | Used for |
|---|---|
| `v1/currentConditions:lookup` | Current temperature, feels-like, humidity, wind, UV, cloud cover |
| `v1/forecast/hours:lookup` | 24-hour forecast strip |
| `v1/forecast/days:lookup` | 10-day forecast with highs/lows, precipitation, sun events |
| Geocoding API | Turning a typed place name into coordinates |

For direct access to raw WeatherNext model data, see
`weathernext_bigquery.py`, a standalone example that queries the WeatherNext
BigQuery dataset (requires allowlist access and `google-cloud-bigquery`).

## Setup

1. In the [Google Cloud Console](https://console.cloud.google.com/), create or
   pick a project and enable the **Weather API** and **Geocoding API**, then
   create an API key (APIs & Services → Credentials).
2. Install and run:

   ```bash
   pip install -r requirements.txt
   export GOOGLE_MAPS_API_KEY="your-key-here"
   python app.py
   ```

3. Open http://127.0.0.1:5000/weather and search for a place. A units toggle
   (°C/°F) is next to the search box.

Deployment uses the existing `Procfile` (`gunicorn app:app`); set
`GOOGLE_MAPS_API_KEY` in the host's environment. The key is only ever used
server-side and is never sent to the browser.
