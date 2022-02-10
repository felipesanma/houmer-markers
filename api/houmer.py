from pydantic import BaseModel

import config
from database import BasicQuerys

params = dict(config.get_env())


class Houmer(BaseModel):

    """
    Class to represent the houmer object
    """

    id: int

    def update_markers(self, lat: float, lon: float):
        insert = f"""
        insert into {params["TABLE_HOUMER_MARKERS"]} (lat, lon, houmer_id)
        values ({lat}, {lon}, {self.id})
        """

        return BasicQuerys(insert).insert()

    def properties_visited(self, date: str) -> list:

        query = f"""
        SELECT ha.start_time, ha.end_time, ha.duration, pm.property_id, pm.lat, pm.lon 
        FROM {params["TABLE_HOUMER_IN_PROPERTY_ACTIVITY"]} AS ha 
        INNER JOIN {params["TABLE_PROPERTIES"]} AS pm
        ON ha.property_id = pm.property_id 
        AND ha.houmer_id = {self.id}
        AND ha.start_time BETWEEN '{date} 00:00:00' AND '{date} 23:59:59';
        """
        fetched, data = BasicQuerys(query).select()

        return data

    def speed_warnings(self, speed: float, date: str) -> list:

        query = f"""
        SELECT start_time, end_time, duration, start_lat, start_lon, end_lat, end_lon, distance_km, velocity_km_hr FROM {params["TABLE_HOUMER_ACTIVITY"]}
        WHERE velocity_km_hr > {speed}
        AND houmer_id = {self.id}
        AND start_time BETWEEN '{date} 00:00:00' AND '{date} 23:59:59';
        """
        fetched, data = BasicQuerys(query).select()

        return data
