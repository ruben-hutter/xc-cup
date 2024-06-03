import pytest
from unittest import mock

from xc_cup_ranker import get_data_and_take_off_site


def test_get_data_and_take_off_site_valid():
    event_id = 1
    date, take_off_site = get_data_and_take_off_site(event_id)
    assert date == "2024-04-06"
    assert take_off_site == "Monte Tamaro"


def test_get_data_and_take_off_site_invalid():
    event_id = 999
    with mock.patch('sys.exit') as mock_exit:
        date, take_off_site = get_data_and_take_off_site(event_id)
        assert date is None
        assert take_off_site is None
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    pytest.main()
