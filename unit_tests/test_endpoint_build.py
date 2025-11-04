import json
from unittest.mock import patch
import pytest
import requests


@pytest.fixture(name='sample_data_response')
def fixture_sample_data_response():
    with open("fake_response.json", 'r') as file:
        data = json.load(file)
    return data


@pytest.fixture(autouse=True)
def mock_requests_get(sample_data_response):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_data_response
        yield mock_get

def test_endpoint_build(sample_data_response):
    sample_endpoint = "https://api.open-meteo.com/v1/forecast?latitude=52.37&longitude=4.89&hourly=temperature_2m,precipitation&timezone=Europe/Amsterdam"

def test_response(sample_data_response):  # not actually testing anything yet as response is always equals to sample_data_response
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.37&longitude=4.89&hourly=temperature_2m,precipitation&timezone=Europe/Amsterdam")
    assert response.status_code == 200
    data = response.json()
    assert data == sample_data_response
