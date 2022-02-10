from config import get_env
from database import BasicQuerys
from geo_calculator import distance_from_lat_lon_in_km, get_bounding_circle

params = get_env()


def get_previous_markers(houmer_id: int) -> tuple:
    query = f"""
    SELECT * FROM {params["TABLE_HOUMER_MARKERS"]} 
    WHERE houmer_id = {houmer_id}
    ORDER BY marker_id DESC
    LIMIT 2;
    """
    return BasicQuerys(query).select()


def get_actual_markers(houmer_id: int) -> tuple:

    query = f"""
    SELECT * FROM {params["TABLE_HOUMER_MARKERS"]} 
    WHERE houmer_id = {houmer_id}
    ORDER BY marker_id DESC
    LIMIT 1;
    """
    return BasicQuerys(query).select()


def get_properties_in_boundary(
    lat_min: float, lat_max: float, lon_min: float, lon_max: float
) -> tuple:

    query = f"""SELECT * FROM {params["TABLE_PROPERTIES"]}
    WHERE lat between {lat_min} And {lat_max}
    AND lon between {lon_min} And {lon_max};
    """

    return BasicQuerys(query).select()


def get_houmer_in_property(marker_id: int):

    query = f"""
    SELECT property_id FROM {params["TABLE_HOUMER_IN_PROPERTY"]} 
    WHERE houmer_marker_id = {marker_id}
    """
    return BasicQuerys(query).select()


def insert_in_property(houmer_id: int, property_id: int, houmer_marker_id: int) -> bool:

    insert = f"""
    insert into {params["TABLE_HOUMER_IN_PROPERTY"]} (houmer_id, property_id, houmer_marker_id)
    values({houmer_id}, {property_id}, {houmer_marker_id});
    """

    return BasicQuerys(insert).insert()


def update_houmer_markers(marker_id: int, in_property: int) -> bool:

    update = f"""
    UPDATE {params["TABLE_HOUMER_MARKERS"]}
    SET in_property = {in_property}
    WHERE marker_id = {marker_id};
    """

    return BasicQuerys(update).update()


def insert_houmer_in_property(
    houmer_id: int, radius_boundary: float, max_distance: float
):

    result = False
    fetched, actual_markers = get_actual_markers(houmer_id)

    if fetched and len(actual_markers) == 1:

        houmer_data = actual_markers[0]
        lat_min, lat_max, lon_min, lon_max = get_bounding_circle(
            houmer_data["lat"], houmer_data["lon"], radius_boundary
        )
        fetched, properties = get_properties_in_boundary(
            lat_min, lat_max, lon_min, lon_max
        )

        if fetched and len(properties) > 0:

            start_lat = houmer_data["lat"]
            start_lon = houmer_data["lon"]

            q_properties = [
                prop
                for prop in properties
                if distance_from_lat_lon_in_km(
                    start_lat, start_lon, prop["lat"], prop["lon"]
                )
                <= max_distance
            ]

            if len(q_properties) > 0:

                new_state = update_houmer_markers(houmer_data["marker_id"], 1)

                for property in q_properties:

                    insert_in_property(
                        houmer_data["houmer_id"],
                        property["property_id"],
                        houmer_data["marker_id"],
                    )

                result = True if new_state else False

    return result


def insert_houmer_in_property_activity(houmer_id: int):

    result = False
    fetched, houmer_markers = get_previous_markers(houmer_id)

    if fetched and len(houmer_markers) == 2:

        previuos_in_property = houmer_markers[1]["in_property"]
        actual_in_property = houmer_markers[0]["in_property"]

        if previuos_in_property == 1 and actual_in_property == 0:

            start_time = houmer_markers[1]["time_stamp"]
            end_time = houmer_markers[0]["time_stamp"]
            duration = end_time - start_time

            fetched, properties_id = get_houmer_in_property(
                houmer_markers[1]["marker_id"]
            )

            for property_id in properties_id:

                insert = f"""
                insert into {params["TABLE_HOUMER_IN_PROPERTY_ACTIVITY"]} (start_time, end_time, duration, houmer_id, property_id)
                values('{start_time}', '{end_time}', '{duration}', {houmer_id}, {property_id['property_id']});
                """
                msql_insert = BasicQuerys(insert).insert()
            result = True if msql_insert else False

    return result
