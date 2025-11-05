# Add your imports here
import json
import logging

from src.config_parser.config_parser import ConfigParser



def parametrize():
    # Implement the parametrize logic here
    # 1. Load and validate workload.json configuration file
    # 2. Parse ISO 8601 duration format from time_increment field (e.g., +P1DT00H00M00S)
    # 3. Generate list of dates between begin_date and end_date using time_increment
    # 4. Create tasks for each location and date combination
    # 5. Write tasks to tasks.json file for use in scrape and transform stages
    config = ConfigParser()
    dates = config.list_time_interval()
    locations = list(config.get_locations())
    tasks = {"tasks": []}

    for location in locations:
        tasks["tasks"].append({"location": location, "dates": dates})

    with open('tasks.json', 'w') as task_file:
        json.dump(tasks, task_file, indent=4)

    logging.info("Tasks written to tasks.json file.")
    logging.info(f"Begin Date: {config.begin_date}")
    logging.info(f"End Date: {config.end_date}")
    logging.info(f"Generated Dates: {dates}")


if __name__ == "__main__":
    parametrize()