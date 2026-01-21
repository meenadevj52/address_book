import math
import requests
from typing import Optional, Tuple

from src.core.settings import settings


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert a human-readable address to latitude and longitude using OpenStreetMap Nominatim.

    Returns a tuple (latitude, longitude) if found, otherwise None.
    """
    url = settings.geocode_url
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "address-book-app"}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return None

    data = response.json()
    if not data:
        return None

    return float(data[0]["lat"]), float(data[0]["lon"])


def haversine_distance(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:
    """
    Calculate the great-circle distance in kilometers between two geographic coordinates.
    """
    earth_radius_km = 6371.0

    lat1_rad = math.radians(latitude_1)
    lat2_rad = math.radians(latitude_2)
    delta_lat_rad = math.radians(latitude_2 - latitude_1)
    delta_lon_rad = math.radians(longitude_2 - longitude_1)

    a = (
        math.sin(delta_lat_rad / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon_rad / 2) ** 2
    )

    central_angle = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_km * central_angle
