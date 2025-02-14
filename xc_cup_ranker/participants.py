import csv

from xc_cup_ranker.config import DATA_DIR
from xc_cup_ranker.utils import check_file_exists_and_not_empty, logger


def get_participants(year: int, event_id: int) -> set[str]:
    """
    Get participants for an event from a CSV file
    :param year: Year of the event
    :param event_id: ID of the event
    :return: Set of participants
    """
    # TODO: maybe get participants from `swissleague.ch`
    participants = set()
    participants_file = DATA_DIR / str(year) / "participants" / f"{event_id}.csv"

    check_file_exists_and_not_empty(participants_file)

    with participants_file.open(newline="") as f:
        logger.debug(f"Reading participants from {participants_file}")
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            participants.add(row[0])

    assert len(participants) > 0

    return participants
