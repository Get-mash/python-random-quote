"""BMW X5 car listings finder for Spain (Barcelona & Madrid)."""

import sys
from car_scraper import CochesNetScraper


def main(show_demo=False):
    """
    Fetch and display BMW X5 listings from Coches.net.

    Args:
        show_demo: If True, show example listings instead of fetching
    """
    print("=" * 75)
    print("🚗 BMW X5 Listings - Barcelona & Madrid")
    print("=" * 75)
    print()

    scraper = CochesNetScraper()
    print("📍 Search Criteria:")
    print("   • Model: BMW X5")
    print("   • Fuel: Diesel")
    print("   • Age: ~5 years (2019-2020)")
    print("   • Mileage: ≤120,000 km")
    print("   • Condition: No accidents")
    print("   • Location: Barcelona (08) & Madrid (28)")
    print()

    # Try to fetch real listings
    print("⏳ Fetching listings from Coches.net...")
    listings = scraper.fetch_listings(limit=5) if not show_demo else []

    if not listings:
        print()
        if show_demo:
            print("📝 Showing example listings format:")
            listings = scraper.get_demo_listings()
        else:
            print("❌ Could not fetch live listings (Coches.net blocks automated access)")
            print()
            print("🔗 To find real listings, visit directly:")
            search_url = scraper.get_search_url()
            print(f"   {search_url}")
            print()
            print("Or search manually on Coches.net:")
            print("   1. Go to https://www.coches.net")
            print("   2. Select: Manufacturer → BMW")
            print("   3. Select: Model → X5")
            print("   4. Select: Fuel → Diesel")
            print("   5. Select: Year → 2019-2020")
            print("   6. Set: Mileage → Up to 120,000 km")
            print("   7. Set: Location → Barcelona or Madrid")
            print("   8. Filter: Sin accidentes (No accidents)")
            print()
            print("💡 TIP: Run 'python get-quote.py demo' to see example format")
            return

    print(f"✅ Found {len(listings)} listings:\n")

    for i, listing in enumerate(listings, 1):
        print(f"{'─' * 75}")
        print(f"🔹 LISTING {i}")
        print(f"{'─' * 75}")
        print(f"Title:    {listing.title}")
        print(f"Price:    {listing.price}")
        print(f"Year:     {listing.year}")
        print(f"Mileage:  {listing.mileage}")
        print(f"Location: {listing.location}")
        print(f"Link:     {listing.link}")
        print()


if __name__ == "__main__":
    # Check if user passed "demo" argument
    demo_mode = len(sys.argv) > 1 and sys.argv[1].lower() == "demo"
    main(show_demo=demo_mode)
