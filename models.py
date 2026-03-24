"""Data models for car listings."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CarListing:
    """Represents a BMW X5 car listing."""

    title: str
    price: str
    mileage: str
    location: str
    year: str
    link: str

    def __str__(self) -> str:
        """Format listing for display."""
        return (
            f"Title: {self.title}\n"
            f"Price: {self.price}\n"
            f"Year: {self.year}\n"
            f"Mileage: {self.mileage}\n"
            f"Location: {self.location}\n"
            f"Link: {self.link}\n"
        )
