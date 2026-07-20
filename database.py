from __future__ import annotations

import os
import sys

import psycopg
from dotenv import load_dotenv


# Load variables from the private .env file.
load_dotenv()


def get_database_config() -> dict[str, str]:
    """Read and validate PostgreSQL configuration."""

    config = {
        "host": os.getenv("DB_HOST", ""),
        "port": os.getenv("DB_PORT", ""),
        "dbname": os.getenv("DB_NAME", ""),
        "user": os.getenv("DB_USER", ""),
        "password": os.getenv("DB_PASSWORD", ""),
    }

    missing_variables = [
        key for key, value in config.items()
        if not value
    ]

    if missing_variables:
        missing_names = ", ".join(missing_variables)
        raise ValueError(
            f"Missing database configuration: {missing_names}"
        )

    return config


def test_database_connection() -> bool:
    """Connect to PostgreSQL and verify the weather_data table."""

    try:
        config = get_database_config()

        with psycopg.connect(**config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT current_database(), current_user;
                    """
                )

                database_name, database_user = cursor.fetchone()

                cursor.execute(
                    """
                    SELECT to_regclass('public.weather_data');
                    """
                )

                table_name = cursor.fetchone()[0]

        print("PostgreSQL connection successful.")
        print(f"Database: {database_name}")
        print(f"User: {database_user}")

        if table_name:
            print("Table found: weather_data")
            return True

        print("Connection worked, but weather_data was not found.")
        return False

    except ValueError as error:
        print(f"Configuration error: {error}")
        return False

    except psycopg.Error as error:
        print("PostgreSQL connection failed.")
        print(f"Error: {error}")
        return False


if __name__ == "__main__":
    connection_successful = test_database_connection()

    if connection_successful:
        sys.exit(0)

    sys.exit(1)