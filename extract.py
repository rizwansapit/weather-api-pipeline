from __future__ import annotations

import requests


API_URL = "https://api.open-meteo.com/v1/forecast"

LOCATION_NAME = "Penampang"
LATITUDE = 5.9167
LONGITUDE = 116.1167

PARAMETERS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "temperature_2m,precipitation",
    "timezone": "Asia/Kuching",
    "forecast_days": 1,
}


def fetch_weather_data() -> dict:
    """Request hourly weather data from Open-Meteo."""

    response = requests.get(
        API_URL,
        params=PARAMETERS,
        timeout=30,
    )

    response.raise_for_status()

    print("API request successful.")
    print(f"HTTP status: {response.status_code}")
    print(f"Request URL: {response.url}")

    return response.json()


if __name__ == "__main__":
    try:
        weather_data = fetch_weather_data()

        print("\nTop-level JSON keys:")
        print(weather_data.keys())

    except requests.RequestException as error:
        print("API request failed.")
        print(f"Error: {error}")