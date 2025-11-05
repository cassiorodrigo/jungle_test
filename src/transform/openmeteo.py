# Add your imports here
import json
import logging
from pathlib import Path
from typing import Generator

import pandas as pd

from src import load_file_path
from src.config_parser.config_parser import ConfigParser




# Add any utility functions here if needed

class Transform(ConfigParser):
    def __init__(self):
        super().__init__()
        self.tasks_path = load_file_path('tasks.json')
        with open(self.tasks_path, 'r') as task_file:
            self.tasks = json.load(task_file)
        self.number_of_tasks = len(self.tasks.get("tasks", []))
        if self.number_of_tasks < 1:
            raise ValueError("No tasks found in tasks.json file.")

    @property
    def _data_dir(self) -> Path:
        current_dir = Path.cwd()
        found = (current_dir / "data").is_dir()
        max_iterations = 5
        iterations = 0
        while iterations < max_iterations and not found:
            current_dir = current_dir.parent
            found = (current_dir / "data").is_dir()
            iterations += 1
        return current_dir / "data"

    def merge_data(self, location):
        raw_path = self._data_dir / 'raw' / location
        structured_path = self._data_dir / 'structured' / location
        daily_files = sorted(raw_path.glob('*.parquet'))
        monthly_files = sorted(structured_path.glob('*.parquet'))
        daily_dfs = [pd.read_parquet(f, engine='pyarrow') for f in daily_files]
        daily_df = pd.concat(daily_dfs)
        monthly_dfs = [pd.read_parquet(f, engine='pyarrow') for f in monthly_files]
        monthly_df = pd.concat(monthly_dfs)
        merged = pd.concat([monthly_df, daily_df])
        merged.drop('time', axis=1, inplace=True)

        file_path = Path(self._data_dir / "merged" / location)
        file_path.mkdir(parents=True, exist_ok=True)

        file_loc = [str(i) for i in monthly_files][0]
        file_loc = file_loc.replace("structured", "merged")
        print(file_loc)

        merged.to_parquet(file_loc, index=False)

        logging.info(f"Wrote merged to {file_loc}")


def transform():
    # Implement the transform logic here
    # 1. Load tasks.json to get the list of dates and locations to process
    # 2. Load all raw LONG format parquet files for the date range
    # 3. Convert LONG format to WIDE format (pivot sensor_name into columns)
    # 4. Load existing historical data from structured_output_dir
    # 5. Merge new data with historical data (handle duplicates and schema differences)
    # 6. Write monthly parquet files to structured_output_dir
    t = Transform()
    print(f"Number of tasks to process: {t.number_of_tasks}")
