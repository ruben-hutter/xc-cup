import csv

from xc_cup_ranker.config import OUTPUT_DIR
from xc_cup_ranker.utils import logger


def export_flights(
    flights: dict[str, dict[str, str]],
    year: int,
    date: str,
    take_off_site: str,
    to_pdf: bool = False,
):
    """
    Export flights to CSV
    :param flights: Dictionary of flights
    :param year: Year of the event
    :param date: Date of the event
    :param take_off_site: Take off site of the event
    :param to_pdf: Export to PDF
    """
    logger.info("Exporting flights to CSV...")

    take_off_site = take_off_site.replace(" ", "_").lower()

    # Create output folder if it doesn't exist
    output_path = OUTPUT_DIR / str(year)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / f"{date}_{take_off_site}.csv"
    with file_path.open("w", newline="") as f:
        writer = csv.writer(f)
        header = [
            "Rank",
            "Take off time",
            "Pilot name",
            "Take off site",
            "Distance (km)",
            "Route Type",
            "Points",
            "Avg speed (km/h)",
            "Glider",
        ]
        writer.writerow(header)
        for pilot_name, flight in flights.items():
            writer.writerow(
                [
                    flight["rank"],
                    flight["take_off_time"],
                    pilot_name,
                    take_off_site,
                    flight["distance"],
                    flight["route_type"],
                    flight["points"],
                    flight["avg_speed"],
                    flight["glider"],
                ]
            )

    if to_pdf:
        _generate_pdf()

    logger.info("Export complete!")


def _generate_pdf():
    logger.info("Exporting to PDF...")

    # TODO: Implement PDF generation

    logger.info("PDF export complete!")
