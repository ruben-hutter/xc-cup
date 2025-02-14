import argparse
import sys

from xc_cup_ranker.config import CURRENT_YEAR, FIRST_YEAR
from xc_cup_ranker.events import get_date_and_take_off_site
from xc_cup_ranker.export import export_flights
from xc_cup_ranker.scraper import get_flights
from xc_cup_ranker.utils import logger, set_verbose_mode


def args_parser():
    parser = argparse.ArgumentParser(description="Create XC Cup ranking for an event")
    parser.add_argument("event_id", type=int, help="event id as in events.csv")
    parser.add_argument("-y", "--year", type=int, help="year")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose mode"
    )
    parser.add_argument("--pdf", action="store_true", help="export to PDF")
    return parser.parse_args()


def main():
    year = CURRENT_YEAR

    args = args_parser()

    if args.verbose:
        set_verbose_mode(True)

    event_id = args.event_id
    if event_id < 1:
        logger.error("Invalid event id")
        sys.exit(1)

    if args.year:
        if args.year < FIRST_YEAR or args.year > CURRENT_YEAR:
            logger.error("Invalid year")
            sys.exit(1)
        year = args.year

    if not (date_and_take_off := get_date_and_take_off_site(year, event_id)):
        logger.error("Event not found")
        sys.exit(1)
    date, take_off_site = date_and_take_off

    flights = get_flights(year, event_id, date, take_off_site)

    if args.pdf:
        export_flights(flights, year, date, take_off_site, to_pdf=True)
    else:
        export_flights(flights, year, date, take_off_site)


if __name__ == "__main__":
    main()
