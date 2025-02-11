import pytest
from pathlib import Path
from unittest.mock import patch

import xc_cup_ranker

TEST_DATA_DIR = Path(__file__).parent / "data"

@pytest.fixture(autouse=True)
def patch_data_dir():
    with patch.object(xc_cup_ranker, "DATA_DIR", TEST_DATA_DIR):
        yield


@patch.object(xc_cup_ranker, "event_id", 1)
@patch.object(xc_cup_ranker, "year", 2024)
def test_get_date_and_take_off_site_valid():
    date, take_off_site = xc_cup_ranker.get_date_and_take_off_site()
    assert date == "2024-04-06"
    assert take_off_site == "Monte Tamaro"


@patch.object(xc_cup_ranker, "event_id", 0)
@patch.object(xc_cup_ranker, "year", 2024)
def test_get_date_and_take_off_site_invalid():
    date, take_off_site = xc_cup_ranker.get_date_and_take_off_site()
    assert date is None
    assert take_off_site is None


@patch.object(xc_cup_ranker, "event_id", 1)
@patch.object(xc_cup_ranker, "year", 2024)
def test_get_participants_valid():
    participants = xc_cup_ranker.get_participants()
    assert len(participants) == 3
    assert "Ruben Hutter" in participants


@patch.object(xc_cup_ranker, "event_id", -1)
@patch.object(xc_cup_ranker, "year", 2024)
def test_get_participants_event_id_invalid():
    with pytest.raises(SystemExit) as exit_info:
        xc_cup_ranker.get_participants()

    assert exit_info.value.code == 1


@patch.object(xc_cup_ranker, "event_id", 1)
@patch.object(xc_cup_ranker, "year", 2023)
def test_get_participants_year_invalid():
    with pytest.raises(SystemExit) as exit_info:
        xc_cup_ranker.get_participants()

    assert exit_info.value.code == 1


@patch.object(xc_cup_ranker, "event_id", 2)
@patch.object(xc_cup_ranker, "year", 2024)
def test_get_participants_list_empty():
    with pytest.raises(SystemExit) as exit_info:
        xc_cup_ranker.get_participants()

    assert exit_info.value.code == 1

