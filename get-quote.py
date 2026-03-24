"""BMW X5 car listings finder for Spain (Barcelona & Madrid)."""

from car_scraper import CochesNetScraper


def main():
    """Fetch and display BMW X5 listings from Coches.net."""
    print("=" * 70)
    print("BMW X5 Listings - Barcelona & Madrid")
    print("=" * 70)
    print()

    scraper = CochesNetScraper()
    print("Fetching BMW X5 listings from Coches.net...")
    print("Criteria: ~5 years old, diesel, ≤120,000 km, no accidents")
    print()

    listings = scraper.fetch_listings(limit=5)

    if not listings:
        print("No listings found. Please check your internet connection or try again later.")
        return

    print(f"Found {len(listings)} listings:\n")

    for i, listing in enumerate(listings, 1):
        print(f"--- Listing {i} ---")
        print(listing)
        print()


if __name__ == "__main__":
    main()
