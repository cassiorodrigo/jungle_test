import pytest

from src.config_parser.config_parser import ConfigParser


@pytest.fixture(name="config_parser")
def fixture_config_parser():
    config_parser = ConfigParser(config_file='../workload.json')
    return config_parser

def test_begin_date(config_parser):
    expected = "2024-10-16"
    assert config_parser.begin_date == expected


def test_date_list(config_parser):
    list_dates = config_parser.list_time_interval()
    assert list_dates == ["2024-10-16", "2024-10-17", "2024-10-18"]