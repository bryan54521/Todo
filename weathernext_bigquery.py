"""Optional: query raw WeatherNext model forecasts from BigQuery.

The WeatherNext models (https://developers.google.com/weathernext/guides/models)
are published as BigQuery datasets via Analytics Hub. Access requires:

1. A Google Cloud project with the BigQuery API enabled.
2. Requesting access via the WeatherNext Data Request form (see
   https://developers.google.com/weathernext/guides/bigquery) and linking the
   dataset from Analytics Hub into your project.
3. Local auth:  gcloud auth application-default login
4. pip install google-cloud-bigquery  (not in requirements.txt — the web app
   does not need it; the app uses the Weather API instead.)

Usage:
    python weathernext_bigquery.py <project_id> [dataset.table] [lat] [lng]

The default table name below matches the WeatherNext Graph sample dataset;
adjust it to whatever name you gave the linked dataset in your project.
"""

import sys

from google.cloud import bigquery

DEFAULT_TABLE = "weathernext_graph_forecasts.59572747_4_0"

QUERY = """
SELECT
  init_time,
  forecast.time AS valid_time,
  forecast.`2m_temperature` - 273.15 AS temp_c,
  forecast.total_precipitation_12hr AS precip_m,
  forecast.`10m_u_component_of_wind` AS wind_u,
  forecast.`10m_v_component_of_wind` AS wind_v
FROM `{table}` AS t, UNNEST(t.forecast) AS forecast
WHERE ST_DWITHIN(t.geography, ST_GEOGPOINT(@lng, @lat), 25000)
ORDER BY init_time DESC, valid_time
LIMIT 40
"""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    project = sys.argv[1]
    table = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_TABLE
    lat = float(sys.argv[3]) if len(sys.argv) > 3 else 40.7128
    lng = float(sys.argv[4]) if len(sys.argv) > 4 else -74.0060

    client = bigquery.Client(project=project)
    job = client.query(
        QUERY.format(table=f"{project}.{table}"),
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("lat", "FLOAT64", lat),
                bigquery.ScalarQueryParameter("lng", "FLOAT64", lng),
            ]
        ),
    )
    for row in job.result():
        print(
            f"{row.valid_time}  temp={row.temp_c:6.1f}°C  "
            f"precip={row.precip_m or 0:.4f}m  wind=({row.wind_u:.1f}, {row.wind_v:.1f}) m/s"
        )


if __name__ == "__main__":
    main()
