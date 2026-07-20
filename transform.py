from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import requests

from extract import LOCATION_NAME, fetch_weather_data


WeatherRecord = dict[str, Any]


def transform_weather_data(
    weather_data: dict[str, Any],
) -> list[WeatherRecord]:
    """Transform Open-Meteo arrays into individual weather records."""

    hourly_data = weather_data.get("hourly")

    if not isinstance(hourly_data, dict):
        raise ValueError("The API response does not contain hourly data.")

    required_fields = [
        "time",
        "temperature_2m",
        "precipitation",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in hourly_data
    ]

    if missing_fields:
        missing_text = ", ".join(missing_fields)

        raise ValueError(
            f"Missing hourly fields: {missing_text}"
        )

    times = hourly_data["time"]
    temperatures = hourly_data["temperature_2m"]
    precipitation_values = hourly_data["precipitation"]

    if not all(
        isinstance(values, list)
        for values in [
            times,
            temperatures,
            precipitation_values,
        ]
    ):
        raise ValueError("Hourly weather fields must be lists.")

    array_lengths = {
        len(times),
        len(temperatures),
        len(precipitation_values),
    }

    if len(array_lengths) != 1:
        raise ValueError(
            "Hourly weather arrays have different lengths."
        )

    timezone_name = weather_data.get(
        "timezone",
        "Asia/Kuching",
    )

    try:
        local_timezone = ZoneInfo(timezone_name)

    except ZoneInfoNotFoundError as error:
        raise ValueError(
            f"Unknown timezone: {timezone_name}"
        ) from error

    weather_records: list[WeatherRecord] = []

    for time_value, temperature, precipitation in zip(
        times,
        temperatures,
        precipitation_values,
    ):
        recorded_time = datetime.fromisoformat(time_value)

        if recorded_time.tzinfo is None:
            recorded_time = recorded_time.replace(
                tzinfo=local_timezone
            )
        else:
            recorded_time = recorded_time.astimezone(
                local_timezone
            )

        record: WeatherRecord = {
            "location_name": LOCATION_NAME,
            "recorded_time": recorded_time,
            "temperature_c": (
                float(temperature)
                if temperature is not None
                else None
            ),
            "rainfall_mm": (
                float(precipitation)
                if precipitation is not None
                else None
            ),
        }

        weather_records.append(record)

    return weather_records

def display_transformed_records(
    weather_records: list[WeatherRecord],
    limit: int = 5,
) -> None:
    """Display a small sample of transformed records."""

    print("\nTransformation successful")
    print("-------------------------")
    print(f"Total clean records: {len(weather_records)}")

    print("\nFirst transformed records")
    print("-------------------------")

    for record in weather_records[:limit]:
        print(
            f"Location: {record['location_name']} | "
            f"Time: {record['recorded_time'].isoformat()} | "
            f"Temperature: {record['temperature_c']} °C | "
            f"Rainfall: {record['rainfall_mm']} mm"
        )

if __name__ == "__main__":
    try:
        api_weather_data = fetch_weather_data()

        transformed_records = transform_weather_data(
            api_weather_data
        )

        display_transformed_records(
            transformed_records
        )

    except requests.RequestException as error:
        print("API request failed.")
        print(f"Error: {error}")

    except ValueError as error:
        print("Weather transformation failed.")
        print(f"Error: {error}")