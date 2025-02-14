# XC-Cup Ranker

Automatically generate ranking lists for Swissleague XC-Cup events by scraping flight data from XContest.

## Overview

The XC Cup Ranker project aims to extract flight data from XContest and calculate rankings for Swissleague XC-Cup events based on pilot performances. This tool provides a convenient way to track top performers and event standings using automated data processing.

## Features

- **Web Scraping**: Utilizes web scraping techniques to retrieve flight data from XContest.
- **Ranking Calculation**: Calculates rankings based on specified criteria (e.g. flight distance, event-specific performance metrics).
- **Data Visualization**: Presents rankings in a clear and informative format.

## Getting Started

Follow these instructions to set up and run the XC-Cup Ranker locally.

### Prerequisites

- Python 3.10 or higher
- `uv` for dependency management (recommended)
- Alternatively, `virtualenv` or `conda` for manual setup

### Installation

#### Using `uv` (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/ruben-hutter/xc-cup-ranker.git
   cd xc-cup-ranker
   ```

2. Create a virtual environment using `uv`:

   ```bash
   uv venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows (CMD/PowerShell)
   ```

3. Install dependencies:

   ```bash
   uv pip sync
   ```

#### Using `virtualenv` (Manual Setup)

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows (CMD/PowerShell)
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

#### Using `conda`

1. Create and activate a new Conda environment:

   ```bash
   conda create -n xc-cup-env python=3.10
   conda activate xc-cup-env
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the script using one of the provided scripts for your platform:

- **Linux/macOS**:
  ```bash
  ./run.sh <event_id> [-y|--year <year>] [-v|--verbose] [--pdf]
  ```
- **Windows (CMD)**:
  ```bash
  run.bat <event_id> [-y|--year <year>] [-v|--verbose] [--pdf]
  ```
- **Windows (PowerShell)**:
  ```bash
  run.ps1 <event_id> [-y|--year <year>] [-v|--verbose] [--pdf]
  ```

Replace `<event_id>` with the event you want to rank. The optional `-y` or `--year` parameter defaults to the current year. Use `-v` or `--verbose` for additional output details and `--pdf` to generate a PDF report.

## Contributing

Contributions are welcome! Follow these steps to contribute to the project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push the branch (`git push origin feature-branch`).
5. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

