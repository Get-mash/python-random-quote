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

### Fetch real listings from Coches.net:
```bash
python get-quote.py
```

**Note:** Due to anti-bot protection on Coches.net, live scraping may fail (403 Forbidden). The script will display the search URL you can visit directly.

### Show example listings (demo mode):
```bash
python get-quote.py demo
```

This displays 5 example BMW X5 listings with realistic data and proper URLs.

### Example Output (Demo Mode):

```
===========================================================================
🚗 BMW X5 Listings - Barcelona & Madrid
===========================================================================

📍 Search Criteria:
   • Model: BMW X5
   • Fuel: Diesel
   • Age: ~5 years (2019-2020)
   • Mileage: ≤120,000 km
   • Condition: No accidents
   • Location: Barcelona (08) & Madrid (28)

✅ Found 5 listings:

───────────────────────────────────────────────────────────────────────────
🔹 LISTING 1
───────────────────────────────────────────────────────────────────────────
Title:    BMW X5 xDrive30d (2020)
Price:    €47,500
Year:     2020
Mileage:  95,200 km
Location: Barcelona
Link:     https://www.coches.net/anuncio/bmw-x5-xdrive30d-2020-barcelona
```

## How to Find Real Listings

When live scraping is blocked, the script will provide:
1. A direct search URL you can paste into your browser
2. Step-by-step instructions for manual filtering on Coches.net

Or visit directly:
```
https://www.coches.net/cgi-bin/buscar?vrm=BMW&mod=X5&com=2&ano_min=2019&ano_max=2020&km_max=120000&prov=08,28&sinacacc=1&orden=fecha
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

## Notes

- The scraper uses hardcoded filters for BMW X5 diesel vehicles 2019-2020 with max 120k km
- Results are fetched from Coches.net search
