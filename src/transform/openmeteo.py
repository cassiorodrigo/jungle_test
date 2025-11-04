# Add your imports here
import json

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
