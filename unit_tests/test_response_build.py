import json
from unittest.mock import Mock

import pandas as pd
import pytest

import requests

@pytest.fixture(autouse=True)
def fixture_requests(mocker):
    mock_resp = Mock(spec=requests.Response)
    with open("fake_response.json", "r") as file:
        response = json.load(file)
        mock_resp.json.return_value = response
    mock_resp.status_code = 200
    mocker.patch("requests.get", return_value=mock_resp)


def test_call_to_service():
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=52.37&longitude=4.89&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,cloud_cover&start_date=2024-10-16&end_date=2024-10-18&timezone=Europe/Amsterdam"
    response = requests.get(url).json()
    hourly = response['hourly']
    keys = "temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,cloud_cover".split(',')
    df = pd.DataFrame(hourly)
    melted_df = pd.melt(df, id_vars=['time'], var_name='sensor_name', value_name='value')
    print(melted_df.head())
    print(melted_df.tail())


