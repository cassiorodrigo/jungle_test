# Add your imports here
import json
import os
import requests
from src import load_file_path
from src.scraper.endpoint_factory import Endpoint
import pandas as pd

import logging

# Add any utility functions here if needed

def write_parquet(data: dict, output_path):
    pd_data = pd.DataFrame(data['hourly'])  # Convert the data to a pandas DataFrame
    tasks_path = load_file_path('tasks.json')        # get the task location and date from data if available
    pd_data['time'] = pd.to_datetime(pd_data['time'])
    pd_data['date'] = pd_data['time'].dt.date
    for date, group in pd_data.groupby(pd_data['date']):
        group_to_save = group.drop(columns=['date'])
        date = ''.join(str(date).split('-'))
        daily_output_path = f"{output_path}/{date}.parquet"
        group_to_save.to_parquet(daily_output_path, index=False)


def scrape():
    # Implement the API scrape logic here
    # 1. Load tasks.json to get the list of dates and locations to scrape
    # 2. Fetch data from Open-Meteo Archive API for each task
    # 3. Convert API response to LONG format (timestamp, location, sensor_name, value)
    # 4. Write daily parquet files to raw_output_dir
    task_file_path = load_file_path("tasks.json")
    endpoint = Endpoint()
    for req_url in endpoint.build_url():
        try:
            location = req_url.split("timezone=Europe/")[-1]
        except IndexError:
            logging.error(f"Could not parse location from URL: {req_url}")
            location = "unknown"
        print(location)
        response = requests.get(req_url)
        if response.status_code == 200:
            data = response.json()
            directory = f"../../data/raw/{location.lower()}"
            os.makedirs(directory, exist_ok=True)
            write_parquet(data, output_path=f"../../data/raw/{location.lower()}")


        else:
            print(f"Failed to fetch data from {req_url}. Status code: {response.status_code}")
    if task_file_path:
        with open(task_file_path, 'r') as task_file:
            tasks = json.load(task_file)
            print(tasks)
    else:
        raise FileNotFoundError("tasks.json file not found within 4 directory levels.")

    return
