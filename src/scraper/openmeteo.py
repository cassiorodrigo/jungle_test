# Add your imports here
from datetime import datetime
from pathlib import Path

import requests
from src.parametrize import parametrize


# Add any utility functions here if needed


def scrape():
    response = requests.get("https://archive-api.open-meteo.com/v1/archive")  # request string needs to be mounted
    print(response)
    # Implement the API scrape logic here
    # 1. Load tasks.json to get the list of dates and locations to scrape
    # 2. Fetch data from Open-Meteo Archive API for each task
    # 3. Convert API response to LONG format (timestamp, location, sensor_name, value)
    # 4. Write daily parquet files to raw_output_dir
    return


if __name__ == "__main__":
    scrape()