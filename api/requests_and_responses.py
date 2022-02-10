import datetime
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, Field, validator

import config

params = dict(config.get_env())


class Markers(BaseModel):

    """
    A class for validating markers
    """

    lat: float = Field(
        ...,
        title="Latitude",
        description="Latitude of the coordinates. Must be a number between -90 and 90",
        example=80.12345,
    )
    lon: float = Field(
        ...,
        title="Longitude",
        description="Longitude of the coordinates. Must be a number between -180 and 180",
        example=-45.9872,
    )

    @validator("lat")
    @classmethod
    def _latitude_validation(cls, value: float) -> float:
        """
        Validate if the value is a float number between -90 and 90
        """

        if value >= -90 and value <= 90:

            return value

        else:

            raise HTTPException(
                420,
                detail={
                    "exception": "Latitude not Valid",
                    "error": "Latitude must be a number between -90 and 90",
                    "variable_name": "lat",
                },
            )

    @validator("lon")
    @classmethod
    def _longitude_validation(cls, value: float) -> float:
        """
        Validate if the value is a float number between -180 and 180
        """

        if value >= -180 and value <= 180:

            return value

        else:

            raise HTTPException(
                420,
                detail={
                    "exception": "Longitude not Valid",
                    "error": "Longitude must be a number between -180 and 180",
                    "variable_name": "lon",
                },
            )


class ResponseHoumerMarkers(BaseModel):

    """
    Class to represent the response for /houmers/update-markers
    """

    message: str
    houmer_id: int
    success: bool


class ResponsePropertyMarkers(BaseModel):

    """
    Class to represent the response for /properties/update-markers
    """

    message: str
    property_id: int
    success: bool


class StringToDateValidator(BaseModel):

    """
    Class to validate a date-string format "YYYY-MM-DD"
    """

    date: str = Field(
        ...,
        title="String to date validator",
        description="validate a date-string format YYYY-MM-DD",
        example="2022-02-02",
    )

    @validator("date")
    @classmethod
    def date_validator(cls, value: str) -> str:
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return value


class ResponseHoumerInProperties(BaseModel):

    """
    Class to represent the response for /houmers/{houmer_id}/properties_visited
    """

    houmer_id: int
    filter_date: str
    properties_visited: List[dict] = Field(
        ...,
        title="Properties visited",
        description="Properties visited from a houmer's day",
        example=[
            {
                "start_time": "2022-02-01 00:00:00",
                "end_time": "2022-02-01 00:01:00",
                "duration": "00:01:00",
                "property_id": 45,
                "lat": -33.45740056,
                "lon": -70.62717053,
            }
        ],
    )


class ResponseHoumerSpeedWarning(BaseModel):

    """
    Class to represent the response for /houmers/{houmer_id}/properties_visited
    """

    houmer_id: int
    filter_date: str
    speed_filter: float
    positions_warning: List[dict]


update_markers_responses = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "message": "New markers updated successfully",
                    "houmer_id": 1,
                    "success": True,
                }
            }
        }
    },
    420: {
        "description": "Latitude not Valid",
        "content": {
            "application/json": {
                "example": {
                    "exception": "Latitude not Valid",
                    "error": "Latitude must be a number between -90 and 90",
                    "variable_name": "lat",
                }
            }
        },
    },
    421: {
        "description": "Longitude not Valid",
        "content": {
            "application/json": {
                "example": {
                    "exception": "Longitude not Valid",
                    "error": "Longitude must be a number between -180 and 180",
                    "variable_name": "lon",
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [{"loc": ["string"], "msg": "string", "type": "string"}]
                }
            }
        },
    },
}

insert_markers_responses = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "message": "New markers updated successfully",
                    "property_id": 1,
                    "success": True,
                }
            }
        }
    },
    420: {
        "description": "Latitude not Valid",
        "content": {
            "application/json": {
                "example": {
                    "exception": "Latitude not Valid",
                    "error": "Latitude must be a number between -90 and 90",
                    "variable_name": "lat",
                }
            }
        },
    },
    421: {
        "description": "Longitude not Valid",
        "content": {
            "application/json": {
                "example": {
                    "exception": "Longitude not Valid",
                    "error": "Longitude must be a number between -180 and 180",
                    "variable_name": "lon",
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [{"loc": ["string"], "msg": "string", "type": "string"}]
                }
            }
        },
    },
}

properties_visited_responses = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "houmer_id": 8,
                    "filter_date": "2022-02-02",
                    "properties_visited": [
                        {
                            "start_time": "2022-02-01 00:00:00",
                            "end_time": "2022-02-01 00:01:00",
                            "duration": "00:01:00",
                            "property_id": 45,
                            "lat": -33.45740056,
                            "lon": -70.62717053,
                        }
                    ],
                }
            }
        }
    },
    421: {
        "description": "Incorrect date format",
        "content": {
            "application/json": {
                "example": {
                    "exception": "Incorrect data format",
                    "error": "should be YYYY-MM-DD",
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [{"loc": ["string"], "msg": "string", "type": "string"}]
                }
            }
        },
    },
}

speed_warning_responses = {
    200: {
        "content": {
            "application/json": {
                "example": {
                    "houmer_id": 8,
                    "filter_date": "2022-02-02",
                    "positions_warning": [
                        {
                            "start_time": "2022-02-01 00:00:00",
                            "end_time": "2022-02-01 00:01:00",
                            "duration": "00:01:00",
                            "start_lat": -33.45740056,
                            "start_lon": -70.62717053,
                            "end_lat": -33.45799999,
                            "end_lon": -70.62717053,
                            "distance_km": 11.2,
                            "velocity_km_hr": 300.2,
                        }
                    ],
                }
            }
        }
    },
    421: {
        "description": "Incorrect date format",
        "content": {
            "application/json": {
                "example": {
                    "exception": "Incorrect data format",
                    "error": "should be YYYY-MM-DD",
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [{"loc": ["string"], "msg": "string", "type": "string"}]
                }
            }
        },
    },
}
