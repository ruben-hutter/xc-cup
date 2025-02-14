import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_file_exists_and_not_empty(file_path: Path):
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        sys.exit(1)

    if file_path.stat().st_size == 0:
        logger.error(f"File is empty: {file_path}")
        sys.exit(1)


def set_verbose_mode(verbose: bool):
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
