# BMW X5 Car Listings Finder

Find BMW X5 listings in Barcelona and Madrid with specific criteria: diesel fuel, approximately 5 years old (2019-2020), under 120,000 km mileage, and no accident history.

## Features

- Scrapes [Coches.net](https://www.coches.net) for BMW X5 listings
- Filters by location (Barcelona & Madrid), fuel type (diesel), age (~5 years), mileage (≤120k km), and accident history
- Displays top 5 listings in formatted output
- Includes price, year, mileage, location, and listing link

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python get-quote.py
```

Example output:

```
======================================================================
BMW X5 Listings - Barcelona & Madrid
======================================================================

Fetching BMW X5 listings from Coches.net...
Criteria: ~5 years old, diesel, ≤120,000 km, no accidents

Found 5 listings:

--- Listing 1 ---
Title: BMW X5 xDrive30d (2020)
Price: €45,500
Year: 2020
Mileage: 95,000 km
Location: Barcelona
Link: https://www.coches.net/...

--- Listing 2 ---
...
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

## Notes

- The scraper uses hardcoded filters for BMW X5 diesel vehicles 2019-2020 with max 120k km
- Results are fetched from Coches.net search
