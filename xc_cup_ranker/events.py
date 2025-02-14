import csv

from xc_cup_ranker.config import DATA_DIR
from xc_cup_ranker.utils import check_file_exists_and_not_empty, logger


def get_date_and_take_off_site(year: int, event_id: int) -> tuple[str, str] | None:
    """
    Get date and take off site for an event
    :param year: Year of the event
    :param event_id: ID of the event
    :return: Tuple of date and take off site or None if event is not found
    """
    # event_id in csv are integers from 1 to n
    events_file = DATA_DIR / str(year) / "events.csv"

    check_file_exists_and_not_empty(events_file)

    with events_file.open(newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for i, row in enumerate(reader):
            if i == event_id - 1:
                logger.info(f"Event found: {row[1]}, {row[2]}")
                return row[1], row[2]

    return None
