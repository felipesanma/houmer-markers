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


def calc_velocity(dist_km, time_start, time_end):

    diff = time_end - time_start
    days, seconds = diff.days, diff.seconds
    if dist_km == 0 or seconds == 0:
        return 0
    hours = (days * 24) + (seconds / 3600)
    return round(dist_km / hours, 1)
