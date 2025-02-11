# XC-Cup Ranker

Automatically generate ranking lists for Swissleague XC-Cup events by scraping
flight data from XContest.

## Overview

The XC Cup Ranker project aims to extract flight data from XContest and calculate
rankings for Swissleague XC-Cup events based on pilot performances. This tool
provides a convenient way to track top performers and event standings using
automated data processing.

## Features

- **Web Scraping**: Utilizes web scraping techniques to retrieve flight data
from XContest.
- **Ranking Calculation**: Calculates rankings based on specified criteria (e.g.
flight distance, event-specific performance metrics).
- **Data Visualization**: Presents rankings in a clear and informative format.

## Getting Started

Follow these instructions to set up and run the XC-Cup Ranker locally.

### Prerequisites

- Python 3.10 or higher
- Required packages (see `requirements.txt`)

### Usage

1. Clone the repository:

```bash
git clone https://github.com/ruben-hutter/xc-cup-ranker.git
cd xc-cup-ranker
```

2. Install the required packages:

    a) Using **Conda**:

    ```bash
    conda create -n xc-cup-env --file package-list.txt
    ```

    b) Using **virtualenv** (recommended for non-Conda users):

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Linux/macOS
    .venv\Scripts\activate.bat  # Windows (CMD)
    pip install -r requirements.txt
    ```

3. Run the script:

    a) Using the **run script**:

    ```bash
    ./run.sh <event_id> [--year <year>] # Linux/macOS
    run.bat <event_id> [--year <year]   # Windows (CMD)
    run.ps1 <event_id> [--year <year]   # Windows (PowerShell)
    ```

    This script will automatically detect and use an active virtual environment (`.venv`), Conda environment (`xc-cup-env`), or fallback to system Python.

    b) Running manually:

    ```bash
    conda run -n xc-cup-env python xc_cup_ranker.py <event_id> [--year <year>]  # Conda
    python xc_cup_ranker.py <event_id> [--year <year>]  # virtualenv
    ```

Replace `<event_id>` with the event you want to rank. The optional `--year` parameter defaults to the current year.

## Contributing

Contributions are welcome! Follow these steps to contribute to the project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push the branch (`git push origin feature-branch`).
5. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

