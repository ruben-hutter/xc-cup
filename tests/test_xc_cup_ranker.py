from pathlib import Path
from unittest.mock import patch

import pytest
from xc_cup_ranker.events import get_date_and_take_off_site
from xc_cup_ranker.participants import get_participants

TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def patch_data_dir():
    with patch("xc_cup_ranker.config.DATA_DIR", TEST_DATA_DIR):
        yield


@pytest.fixture
def valid_event():
    """Fixture for a valid event"""
    return 2024, 1


@pytest.fixture
def invalid_event():
    """Fixture for an invalid event"""
    return 2024, 0


def test_get_date_and_take_off_site_valid(valid_event):
    """Test retrieving a valid event"""
    year, event_id = valid_event
    event_data = get_date_and_take_off_site(year, event_id)

    assert event_data is not None
    date, take_off_site = event_data
    assert date == "2024-04-06"
    assert take_off_site == "Monte Tamaro"


def test_get_date_and_take_off_site_invalid(invalid_event):
    """Test retrieving an invalid event"""
    year, event_id = invalid_event
    event_data = get_date_and_take_off_site(year, event_id)

    assert event_data is None


def test_get_participants_valid(valid_event):
    """Test retrieving participants for a valid event"""
    year, event_id = valid_event
    participants = get_participants(year, event_id)

    assert len(participants) == 3
    assert "Ruben Hutter" in participants


@pytest.mark.parametrize("event_id", [-1, 999])
def test_get_participants_event_id_invalid(event_id):
    """Test retrieving participants for an invalid event"""
    with pytest.raises(SystemExit) as exit_info:
        get_participants(2024, event_id)

    assert exit_info.value.code == 1


@pytest.mark.parametrize("year", [2000, 3000])
def test_get_participants_year_invalid(year):
    """Test retrieving participants for an invalid year"""
    with pytest.raises(SystemExit) as exit_info:
        get_participants(year, 1)

    assert exit_info.value.code == 1


def test_get_participants_list_empty():
    """Test retrieving participants for an empty event"""
    year = 2024
    event_id = 2

    with pytest.raises(SystemExit) as exit_info:
        get_participants(year, event_id)

    assert exit_info.value.code == 1
