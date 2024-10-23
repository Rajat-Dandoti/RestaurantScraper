# Restaurant Scraper

A simple Python script that scrapes restaurant information from Google Maps for any city.

## Setup

1. Install Python 3.x
2. Install required package:
   ```bash
   pip install selenium
   ```
3. Make sure you have Chrome browser and ChromeDriver installed

## How to Use

1. Run the script:
   ```bash
   python RestaurantScraper.py
   ```
2. Enter a city name when prompted
3. The script will find the top 10 restaurants and save their details to a JSON file

## What It Collects

- Restaurant name
- Description
- Rating
- Number of reviews
- Address
- Cuisine type
- Price level

## How It Works

1. **Search Process**:
    - Opens Google search
    - Searches for "Top 10 restaurants in {city}"
    - Automatically navigates to Google Maps results

2. **Scraping Method**:
    - Identifies restaurant listings using HTML elements
    - Clicks each restaurant to load detailed information
    - Extracts data from the expanded details panel
    - Scrolls automatically to load more results if needed

3. **Data Handling**:
    - Processes one restaurant at a time
    - Stores data in a structured dictionary
    - Saves results to a timestamped JSON file

## Technical Details

- Uses Selenium WebDriver for web automation
- Implements intelligent waiting mechanisms to handle dynamic content
- Includes automatic scrolling to load more results
- Handles missing data gracefully with try-except blocks
- Saves data in JSON format with timestamp: `{city}_restaurants_{timestamp}.json`
- Closes browser automatically after scraping

## Note

This tool is for educational purposes. Please use responsibly and respect Google's terms of service.