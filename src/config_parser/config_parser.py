"""This is the configuration parser module for the application."""

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Generator

import isoduration
from isoduration.types import Duration

from src import load_file_path


class ConfigParser:
    """A class to parse configuration files."""

    def __init__(self, config_file: str | Path | None = None):

        config_path = load_file_path()

        if not config_file:
            self.config_file = config_path
        else:
            self.config_file = config_file
        self._load_config()

    def _load_config(self):
        """Load configuration from a JSON file."""
        try:
            with open(self.config_file, 'r') as file:
                self.config_data = json.load(file)
        except FileNotFoundError:
            print(f"Configuration file {self.config_file} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the configuration file {self.config_file}.")

    @property
    def begin_date(self) -> str:
        """Get the begin date from the configuration."""
        date_config = self._get_date()
        return date_config.get("begin_date", "")

    @property
    def end_date(self) -> str:
        """Get the end date from the configuration."""
        date_config = self._get_date()
        return date_config.get("end_date", "")

    @property
    def get_delta(self) -> Duration:
        """Get the time increment from the configuration."""
        date_config = self._get_date()
        raw_delta = date_config.get("time_increment", "")
        transformed_delta = isoduration.parse_duration(raw_delta)
        return transformed_delta

    def _get_date(self) -> dict:
        """Get the date configuration."""
        return self.config_data.get("date_config", {})

    def get_locations(self) -> Generator[str, None, None]:
        """Get the list of locations from the configuration."""
        for location in self.config_data.get("locations", []):
            yield location.get("name", "")

    @property
    def _list_interval_dates(self) -> list:
        """Generate a list of dates between begin_date and end_date using time_increment."""
        interval = []
        current_date = self.begin_date
        time_increment = self.get_delta
        while self.end_date not in interval:
            interval.append(current_date)
            current_date = date.fromisoformat(current_date)

            days = int(time_increment.date.days)
            hours = int(time_increment.time.hours)
            minutes = int(time_increment.time.minutes)
            seconds = int(time_increment.time.seconds)
            current_date += timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            current_date = current_date.isoformat()
        return interval

    def list_time_interval(self):
        return self._list_interval_dates

    @property
    def location_paths(self):
        """Set the list of locations in the configuration."""
        location_paths = {
            "raw_output_dir": "data/raw/{location_name}/%Y%m%d.parquet",
            "structured_output_dir": "data/structured/{location_name}/%Y%m.parquet"
        }
        raw_dir = location_paths.get("raw_output_dir", "")
        structured_dir = location_paths.get("structured_output_dir", "")

        for location in self.get_locations():
            if location:
                raw_dir.replace("{location_name}", location)
                structured_dir.replace("{location_name}", location)
            yield {location: {"raw_output_dir": raw_dir, "structured_output_dir": structured_dir}}

    @property
    def get_sensors(self) -> list:
        """Get the list of sensors from the configuration."""
        sensors = []
        for location in self.get_locations():
            if not location:
                raise NoLocationError("Location data is missing in the configuration.")
            locations_and_sensors = self.config_data.get("locations")
            for loc in locations_and_sensors:
                if loc.get("name") == location:
                    sensors.extend(loc.get("sensors", []))
        return sensors


class NoLocationError(Exception):
    """Custom exception for missing location data."""
    pass
