# Add your imports here
from datetime import datetime
import json

from pathlib import Path
import isoduration
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)
# Add any utility functions here if needed

def load_json(path: Path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error("No json file found. returning Empty dictionary.")
        return {}
    return data

def generate_dates():
    path = Path("../workload.json")
    data = load_json(path)
    try:
        start = data["date_config"]["begin_date"]
        end = data["date_config"]["end_date"]
        time_increment = data["date_config"]["time_increment"]
    except KeyError as err:
        logging.error("The dictionary key wasnt found. Please, check the configuration file")
        raise err
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    time_increment = isoduration.parse_duration(time_increment)
    dates = []
    curr = start
    while curr <= end:
        dates.append(curr)
        curr += time_increment
    print(dates)
    return dates

def parametrize():
    # Implement the parametrize logic here
    # 1. Load and validate workload.json configuration file
    # 2. Parse ISO 8601 duration format from time_increment field (e.g., +P1DT00H00M00S)
    # 3. Generate list of dates between begin_date and end_date using time_increment
    # 4. Create tasks for each location and date combination
    # 5. Write tasks to tasks.json file for use in scrape and transform stages
    path = Path("../workload.json")
    data = load_json(path)
    locations = [location.get("name") for location in data.get("locations")]

    print(locations)


if __name__ == "__main__":
    parametrize()