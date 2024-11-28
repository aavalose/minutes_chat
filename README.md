# FOMC Minutes Scraper and Analyzer

This project is a tool for scraping, storing, and analyzing Federal Open Market Committee (FOMC) meeting minutes. It includes a web interface for viewing and comparing the minutes using OpenAI's language model.

## Features

- **Scrape and Download**: Automatically download the latest FOMC minutes in PDF format.
- **View and Search**: Display and search through stored minutes using a web interface.
- **Analyze with AI**: Use OpenAI's GPT-4 to analyze and compare excerpts from the minutes.

## Installation

### Prerequisites

- Python 3.7+
- Node.js (for Streamlit)
- OpenAI API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fomc-minutes-scraper.git
   cd fomc-minutes-scraper
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your configuration:
   - Create a `config.py` file with the following variables:
     ```python
     PDF_MINUTES = 'path/to/store/pdf/minutes'
     client = 'your_openai_client'
     ```

## Usage

### Scraping Minutes

Run the `scrapping_minutes.py` script to download the latest FOMC minutes: