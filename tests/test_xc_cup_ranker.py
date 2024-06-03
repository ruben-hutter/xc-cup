from xc_cup_ranker import get_date_and_take_off_site

year = 2024

def test_get_date_and_take_off_site_valid():
    event_id = 1
    date, take_off_site = get_date_and_take_off_site(event_id)
    assert date == "2024-04-06"
    assert take_off_site == "Monte Tamaro"


def test_get_date_and_take_off_site_invalid():
    event_id = 999
    date, take_off_site = get_date_and_take_off_site(event_id)
    assert date is None
    assert take_off_site is None
