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

def display_weather_summary(weather_data: dict) -> None:
    """Display a small summary of the API response."""

    hourly_data = weather_data["hourly"]
    hourly_units = weather_data["hourly_units"]

    times = hourly_data["time"]
    temperatures = hourly_data["temperature_2m"]
    precipitation_values = hourly_data["precipitation"]

    print("\nWeather data received")
    print("---------------------")
    print(f"Location: {LOCATION_NAME}")
    print(
        f"API grid coordinate: "
        f"{weather_data['latitude']}, {weather_data['longitude']}"
    )
    print(f"Timezone: {weather_data['timezone']}")
    print(f"Number of hourly records: {len(times)}")

    temperature_unit = hourly_units["temperature_2m"]
    precipitation_unit = hourly_units["precipitation"]

    print("\nFirst five hourly records")
    print("-------------------------")

    for index in range(min(5, len(times))):
        print(
            f"{times[index]} | "
            f"Temperature: {temperatures[index]} {temperature_unit} | "
            f"Precipitation: "
            f"{precipitation_values[index]} {precipitation_unit}"
        )

if __name__ == "__main__":
    try:
        weather_data = fetch_weather_data()
        display_weather_summary(weather_data)

    except requests.RequestException as error:
        print("API request failed.")
        print(f"Error: {error}")

    except (KeyError, TypeError, ValueError) as error:
        print("The API response has an unexpected structure.")
        print(f"Error: {error}")