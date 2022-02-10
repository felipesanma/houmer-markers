from math import dist

from config import get_env
from database import BasicQuerys
from geo_calculator import calc_velocity, distance_from_lat_lon_in_km

params = get_env()


def get_previous_markers(houmer_id: int) -> tuple:
    query = f"""
    SELECT * FROM {params["TABLE_HOUMER_MARKERS"]} 
    WHERE houmer_id = {houmer_id}
    ORDER BY marker_id DESC
    LIMIT 2;
    """
    return BasicQuerys(query).select()


def insert_houmer_activity(houmer_id: int) -> bool:

    result = False
    fetched, previuos_markers = get_previous_markers(houmer_id)

    if fetched and len(previuos_markers) == 2:

        end_lat = previuos_markers[0]["lat"]
        end_lon = previuos_markers[0]["lon"]
        end_time = previuos_markers[0]["time_stamp"]

        start_lat = previuos_markers[1]["lat"]
        start_lon = previuos_markers[1]["lon"]
        start_time = previuos_markers[1]["time_stamp"]

        duration = end_time - start_time
        distance_km = distance_from_lat_lon_in_km(
            start_lat, start_lon, end_lat, end_lon
        )
        distance_m = distance_km * 1000
        velocity_km_hr = calc_velocity(distance_km, start_time, end_time)

        insert = f"""
        insert into {params["TABLE_HOUMER_ACTIVITY"]} (houmer_id, start_time, end_time, duration, start_lat, start_lon, end_lat, end_lon, distance_m, distance_km, velocity_km_hr)
        values({houmer_id}, '{start_time}', '{end_time}', '{duration}', {start_lat}, {start_lon}, {end_lat}, {end_lon}, {distance_m}, {distance_km}, {velocity_km_hr});
        """
        msql_insert = BasicQuerys(insert).insert()
        result = True if msql_insert else False
    return result
