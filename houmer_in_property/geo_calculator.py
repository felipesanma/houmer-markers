import math
from math import acos, asin, atan2, cos, radians, sin, sqrt

from config import get_env

params = get_env()


def distance_from_lat_lon_in_km(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calculate the Haversine distance.
    Returns
    -------
    distance_in_km : float
    """
    R = int(params["EARTH_RADIUS"])  # Radius of the earth in km
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    rLat1 = radians(lat1)
    rLat2 = radians(lat2)
    a = sin(dLat / 2) * sin(dLat / 2) + cos(rLat1) * cos(rLat2) * sin(dLon / 2) * sin(
        dLon / 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = round(R * c, 1)  # Distance in km
    return d


# Calculate the bounding Circles: http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates


def lat_boundaries(lat: float, distance: float) -> tuple:

    R = int(params["EARTH_RADIUS"])  # Radius of the earth in km
    angular_radius = distance / R  # angular radius
    lat_min = radians(lat) - angular_radius
    lat_max = radians(lat) + angular_radius

    return round(math.degrees(lat_min), 8), round(math.degrees(lat_max), 8)


def lon_boundaries(lat: float, lon: float, distance: float) -> tuple:

    R = int(params["EARTH_RADIUS"])  # Radius of the earth in km
    angular_radius = distance / R  # angular radius
    lat = radians(lat)
    lon = radians(lon)
    lat_t = asin(sin(lat) / cos(angular_radius))
    delta_lon = acos(
        (cos(angular_radius) - sin(lat_t) * sin(lat)) / (cos(lat_t) * cos(lat))
    )
    lon_min = lon - delta_lon
    lon_max = lon + delta_lon

    return round(math.degrees(lon_min), 8), round(math.degrees(lon_max), 8)


def get_bounding_circle(lat: float, lon: float, distance: float) -> tuple:

    lat_min, lat_max = lat_boundaries(lat, distance)
    lon_min, lon_max = lon_boundaries(lat, lon, distance)

    return lat_min, lat_max, lon_min, lon_max
