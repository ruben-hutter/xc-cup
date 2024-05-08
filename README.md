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

- Python 3.6 or higher
- Required packages (see `requirements.txt`)

### Usage

1. Clone the repository:

```bash
git clone https://github.com/ruben-hutter/xc-cup-ranker.git
cd xc-cup-ranker
```

2. Install the required packages:

    a) Using pip:

    ```bash
    pip install -r requirements.txt
    ```

    b) Using conda:

    ```bash
    conda create -n xc-cup-ranker --file package-list.txt
    ```

3. Run the script:

```bash
python scraper.py <event_id>
```

Replace `<event_id>` with the ID of the event you want to rank.

## Contributing

Contributions are welcome! Follow these steps to contribute to the project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push the branch (`git push origin feature-branch`).
5. Create a new pull request.

Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project was inspired by the need to automate XC-Cup rankings.
- Special thanks to the contributors and maintainers of XContest for providing
access to flight data.

