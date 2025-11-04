"""This module defines a factory for creating endpoint instances based on given configurations."""
from typing import Dict, Type, Generator

from src.config_parser.config_parser import ConfigParser


class Endpoint(ConfigParser):
    """Base class for all endpoints."""
    def __init__(self):
        super().__init__()
        self.base_url = "https://archive-api.open-meteo.com/v1/archive"
        self.coordinates = {        # could be dynamic, but for simplicity, hardcoded here.
            "london": (51.51, -0.13),
            "amsterdam": (52.37, 4.89),
        }

    def build_url(self) -> Generator[str]:
        """Build the URL for the endpoint. Assuming hourly data for simplicity."""
        for location in self.get_locations():
            latitude = self.coordinates.get(location)[0]
            longitude = self.coordinates.get(location)[1]
            sensors = ",".join(self.get_sensors)
            url = (f"{self.base_url}?latitude={latitude}&longitude={longitude}"
                   f"&hourly={sensors}"
                   f"&start_date={self.begin_date}"
                   f"&end_date={self.end_date}"
                   f"&timezone=Europe/{location.title()}")
            yield url
