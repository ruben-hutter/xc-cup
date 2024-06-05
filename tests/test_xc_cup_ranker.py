from unittest.mock import patch

import xc_cup_ranker

@patch.object(xc_cup_ranker, 'event_id', 1)
def test_get_date_and_take_off_site_valid():
    date, take_off_site = xc_cup_ranker.get_date_and_take_off_site()
    assert date == "2024-04-06"
    assert take_off_site == "Monte Tamaro"


@patch.object(xc_cup_ranker, 'event_id', 0)
def test_get_date_and_take_off_site_invalid():
    date, take_off_site = xc_cup_ranker.get_date_and_take_off_site()
    assert date is None
    assert take_off_site is None


@patch.object(xc_cup_ranker, 'event_id', 1)
@patch.object(xc_cup_ranker, 'year', 2024)
def test_get_participants_valid():
    participants = xc_cup_ranker.get_participants()
    assert len(participants) == 3
    assert "Ruben Hutter" in participants


@patch.object(xc_cup_ranker, 'event_id', 2)
@patch.object(xc_cup_ranker, 'year', 2024)
def test_get_participants_event_id_invalid():
    participants = xc_cup_ranker.get_participants()
    # TODO: check if program exits and logs error


@patch.object(xc_cup_ranker, 'event_id', 1)
@patch.object(xc_cup_ranker, 'year', 2023)
def test_get_participants_year_invalid():
    participants = xc_cup_ranker.get_participants()
    # TODO: check if program exits and logs error


def test_get_participants_list_empty():
    # TODO: mock existance of empty file
    participants = xc_cup_ranker.get_participants()
    # TODO: check if program exits and logs error
