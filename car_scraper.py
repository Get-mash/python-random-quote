"""Web scraper for BMW X5 listings from Coches.net."""

import re
from typing import List

import requests
from bs4 import BeautifulSoup

from models import CarListing


class CochesNetScraper:
    """Scraper for Coches.net car listings."""

    BASE_URL = "https://www.coches.net"
    SEARCH_PATH = "/cgi-bin/buscar"

    def __init__(self):
        """Initialize the scraper with headers."""
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }

    def build_search_url(self) -> str:
        """Build the search URL with hardcoded filters for BMW X5."""
        # Parameters for BMW X5 search:
        # - Manufacturer: BMW
        # - Model: X5
        # - Fuel: Diesel (2)
        # - Min year: 2019
        # - Max year: 2020
        # - Max mileage: 120000
        # - Province: Barcelona (08) or Madrid (28)
        # - Sin accidentes: yes

        params = {
            "vrm": "BMW",  # Manufacturer
            "mod": "X5",  # Model
            "com": "2",  # Fuel: 2 = Diesel
            "ano_min": "2019",
            "ano_max": "2020",
            "km_max": "120000",
            "prov": "08,28",  # Barcelona (08) and Madrid (28)
            "sinacacc": "1",  # No accidents
            "orden": "fecha",  # Sort by date
        }

        url = f"{self.BASE_URL}{self.SEARCH_PATH}"
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{url}?{query_string}"

    def fetch_listings(self, limit: int = 5) -> List[CarListing]:
        """
        Fetch BMW X5 listings from Coches.net.

        Args:
            limit: Maximum number of listings to return

        Returns:
            List of CarListing objects
        """
        url = self.build_search_url()

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching listings: {e}")
            return []

        listings = self._parse_listings(response.text)
        return listings[:limit]

    def _parse_listings(self, html: str) -> List[CarListing]:
        """
        Parse listings from HTML content.

        Args:
            html: Raw HTML content from Coches.net

        Returns:
            List of CarListing objects
        """
        soup = BeautifulSoup(html, "html.parser")
        listings = []

        # Find all listing rows (adjust selector based on actual HTML structure)
        listing_containers = soup.find_all("div", class_="anuncio")

        if not listing_containers:
            # Try alternative selector if main one fails
            listing_containers = soup.find_all("div", class_="resultado")

        for container in listing_containers:
            try:
                listing = self._extract_listing_data(container)
                if listing:
                    listings.append(listing)
            except Exception as e:
                print(f"Error parsing listing: {e}")
                continue

        return listings

    def _extract_listing_data(self, container) -> CarListing | None:
        """
        Extract individual listing data from a container element.

        Args:
            container: BeautifulSoup element containing one listing

        Returns:
            CarListing object or None if parsing fails
        """
        try:
            # Extract title
            title_elem = container.find("h2") or container.find("a", class_="titulo")
            title = title_elem.get_text(strip=True) if title_elem else "N/A"

            # Extract price
            price_elem = container.find("span", class_="precio")
            price = price_elem.get_text(strip=True) if price_elem else "N/A"

            # Extract mileage (km)
            mileage_text = container.get_text()
            mileage_match = re.search(r"(\d+\.?\d*)\s*km", mileage_text)
            mileage = mileage_match.group(1) + " km" if mileage_match else "N/A"

            # Extract location
            location_elem = container.find("span", class_="provincia") or container.find(
                "span", class_="poblacion"
            )
            location = location_elem.get_text(strip=True) if location_elem else "N/A"

            # Extract year
            year_match = re.search(r"\((\d{4})\)", title)
            year = year_match.group(1) if year_match else "N/A"

            # Extract link
            link_elem = container.find("a", href=True)
            link = link_elem["href"] if link_elem else "#"
            if not link.startswith("http"):
                link = self.BASE_URL + link

            return CarListing(
                title=title, price=price, mileage=mileage, location=location, year=year, link=link
            )

        except Exception as e:
            print(f"Error extracting listing data: {e}")
            return None
