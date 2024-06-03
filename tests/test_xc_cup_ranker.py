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
