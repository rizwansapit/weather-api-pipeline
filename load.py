from __future__ import annotations

import psycopg
import requests

from database import get_database_config
from extract import fetch_weather_data
from transform import WeatherRecord, transform_weather_data


INSERT_WEATHER_SQL = """
    INSERT INTO weather_data (
        location_name,
        record_time,
        temperature_c,
        rainfall_mm
    )
    VALUES (%s, %s, %s, %s);
"""


def load_weather_records(
    weather_records: list[WeatherRecord],
) -> int:
    """Insert transformed weather records into PostgreSQL."""

    if not weather_records:
        raise ValueError("No weather records are available to load.")

    database_config = get_database_config()

    rows_to_insert = [
        (
            record["location_name"],
            record["recorded_time"],
            record["temperature_c"],
            record["rainfall_mm"],
        )
        for record in weather_records
    ]

    with psycopg.connect(**database_config) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(
                INSERT_WEATHER_SQL,
                rows_to_insert,
            )

    return len(rows_to_insert)


def run_pipeline() -> None:
    """Run extraction, transformation, and loading."""

    print("Starting weather data pipeline...")
    print("---------------------------------")

    api_weather_data = fetch_weather_data()

    weather_records = transform_weather_data(
        api_weather_data
    )

    print(
        f"\nTransformed records ready: "
        f"{len(weather_records)}"
    )

    inserted_count = load_weather_records(
        weather_records
    )

    print("\nPostgreSQL loading successful.")
    print(f"Records inserted: {inserted_count}")
    print("\nWeather data pipeline completed.")


if __name__ == "__main__":
    try:
        run_pipeline()

    except requests.RequestException as error:
        print("\nAPI request failed.")
        print(f"Error: {error}")

    except ValueError as error:
        print("\nData validation failed.")
        print(f"Error: {error}")

    except psycopg.Error as error:
        print("\nPostgreSQL loading failed.")
        print(f"Error: {error}")