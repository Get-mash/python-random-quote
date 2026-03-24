"""Web scraper for BMW X5 listings from Coches.net."""

import re
from typing import List
from datetime import datetime

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
        print(f"Fetching from: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            print(f"Response status: {response.status_code}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                print("⚠️  Coches.net is blocking the request (403 Forbidden)")
                print("This is a common anti-bot protection.")
            print(f"Error fetching listings: {e}")
            return []
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return []

        listings = self._parse_listings(response.text)
        if not listings:
            print("⚠️  No listings found. The HTML structure may have changed.")
            print("Tip: Check if Coches.net updated their website design.")

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

        # Try multiple selectors to find listing containers
        listing_containers = (
            soup.find_all("div", class_="anuncio") or
            soup.find_all("article", class_="resultado") or
            soup.find_all("div", class_="resultado") or
            soup.find_all("li", class_="anuncio-item") or
            soup.find_all("div", attrs={"data-anuncio-id": True})
        )

        if not listing_containers:
            print("No listing containers found. Trying alternative search...")
            # Last resort: find all divs with href links
            listing_containers = [
                elem for elem in soup.find_all("a", href=True)
                if "/anuncio/" in elem.get("href", "")
            ]

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
            # Handle if container is an anchor tag directly
            if container.name == "a" and "/anuncio/" in container.get("href", ""):
                # This is a direct listing link
                link = container.get("href", "#")
                if not link.startswith("http"):
                    link = self.BASE_URL + link

                title = container.get_text(strip=True) or "N/A"
                parent = container.find_parent(["div", "li", "article"])
                if parent:
                    container = parent
                else:
                    # Create minimal listing with link we found
                    return CarListing(
                        title=title, price="N/A", mileage="N/A",
                        location="N/A", year="N/A", link=link
                    )

            # Extract title
            title_elem = (
                container.find("h2") or
                container.find("a", class_="titulo") or
                container.find("h3") or
                container.find("span", class_="titulo")
            )
            title = title_elem.get_text(strip=True) if title_elem else "N/A"

            # Extract price - try multiple selectors
            price_elem = (
                container.find("span", class_="precio") or
                container.find("div", class_="precio") or
                container.find("p", class_="precio") or
                container.find(text=re.compile(r"€"))
            )
            price = price_elem.get_text(strip=True) if price_elem else "N/A"

            # Extract mileage (km)
            mileage_text = container.get_text()
            mileage_match = re.search(r"(\d+[.,]?\d*)\s*(?:km|KM)", mileage_text)
            mileage = mileage_match.group(1) + " km" if mileage_match else "N/A"

            # Extract location
            location_elem = (
                container.find("span", class_="provincia") or
                container.find("span", class_="poblacion") or
                container.find("span", class_="location") or
                container.find("p", class_="location")
            )
            location = location_elem.get_text(strip=True) if location_elem else "N/A"

            # Extract year - from title or separate element
            year = "N/A"
            year_match = re.search(r"\b(20\d{2})\b", title)
            if year_match:
                year = year_match.group(1)

            # Extract link - CRITICAL: find actual listing link
            link = "#"
            # Try direct href from container link
            link_elem = container.find("a", href=re.compile(r"/anuncio/"))
            if link_elem:
                link = link_elem.get("href", "#")
            else:
                # Fallback: try any a tag with href
                link_elem = container.find("a", href=True)
                if link_elem:
                    link = link_elem.get("href", "#")

            # Ensure absolute URL
            if link != "#" and not link.startswith("http"):
                link = self.BASE_URL + link

            return CarListing(
                title=title, price=price, mileage=mileage, location=location, year=year, link=link
            )

        except Exception as e:
            print(f"Error extracting listing data: {e}")
            return None

    def get_search_url(self) -> str:
        """
        Get the search URL for browsing listings.

        Returns:
            URL to browse BMW X5 listings on Coches.net
        """
        return self.build_search_url()

    def get_demo_listings(self) -> List[CarListing]:
        """
        Return example listings showing the expected format.
        Useful for demonstration when real scraping fails.

        Returns:
            List of example CarListing objects with realistic data
        """
        return [
            CarListing(
                title="BMW X5 xDrive30d (2020)",
                price="€47,500",
                year="2020",
                mileage="95,200 km",
                location="Barcelona",
                link="https://www.coches.net/anuncio/bmw-x5-xdrive30d-2020-barcelona"
            ),
            CarListing(
                title="BMW X5 xDrive25d (2019)",
                price="€42,800",
                year="2019",
                mileage="108,500 km",
                location="Madrid",
                link="https://www.coches.net/anuncio/bmw-x5-xdrive25d-2019-madrid"
            ),
            CarListing(
                title="BMW X5 xDrive30d (2020)",
                price="€48,900",
                year="2020",
                mileage="87,600 km",
                location="Barcelona",
                link="https://www.coches.net/anuncio/bmw-x5-xdrive30d-2020-barcelona-2"
            ),
            CarListing(
                title="BMW X5 xDrive40d (2019)",
                price="€49,200",
                year="2019",
                mileage="112,900 km",
                location="Madrid",
                link="https://www.coches.net/anuncio/bmw-x5-xdrive40d-2019-madrid"
            ),
            CarListing(
                title="BMW X5 xDrive30d (2019)",
                price="€41,900",
                year="2019",
                mileage="119,500 km",
                location="Barcelona",
                link="https://www.coches.net/anuncio/bmw-x5-xdrive30d-2019-barcelona"
            ),
        ]
