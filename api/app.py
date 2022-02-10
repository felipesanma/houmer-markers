import uvicorn
from fastapi import Body, FastAPI, HTTPException
from pydantic import StrictStr

import config
from database import BasicQuerys
from houmer import Houmer
from rabbitmq import QueueManager
from requests_and_responses import (
    Markers,
    ResponseHoumerInProperties,
    ResponseHoumerMarkers,
    ResponseHoumerSpeedWarning,
    ResponsePropertyMarkers,
    StringToDateValidator,
    insert_markers_responses,
    properties_visited_responses,
    speed_warning_responses,
    update_markers_responses,
)

params = dict(config.get_env())

app = FastAPI(
    title="Houmer Markers",
    description="Houmers API for updating and getting houmer activity",
    version="0.0.1",
    servers=[
        {"url": "http://localhost:8000", "description": "Development Server"},
        {
            "url": "https://mock.example.io",
            "description": "Mock Server",
        },
    ],
)


@app.post(
    "/houmers/{houmer_id}/update-markers",
    name="Houmer Markers",
    summary="Update a new position (latitude and longitude) for a houmer",
    response_description="Message with updated successfully",
    response_model=ResponseHoumerMarkers,
    responses=update_markers_responses,
    tags=["Houmer Markers"],
)
async def update_houmer_markers(houmer_id: int, markers: Markers):

    houmer = Houmer(id=houmer_id)
    res = houmer.update_markers(markers.lat, markers.lon)
    if not res:
        raise HTTPException(status_code=501, detail="Failed on insert to the database")

    await QueueManager().publish_message({"houmer_id": houmer_id}, params["EXCHANGE"])
    return {
        "message": "New markers updated successfully",
        "houmer_id": houmer_id,
        "success": True,
    }


@app.get(
    "/houmers/{houmer_id}/properties_visited",
    name="Houmer in Properties",
    summary="Get all properties visited for a day",
    response_description="List where every element is a json with the property data",
    response_model=ResponseHoumerInProperties,
    responses=properties_visited_responses,
    tags=["Houmer in Properties"],
)
async def properties_visited(houmer_id: int, filter_date: str = Body(..., embed=True)):
    on_date = StringToDateValidator(date=filter_date).date
    result = {"houmer_id": houmer_id, "filter_date": on_date}

    houmer = Houmer(id=houmer_id)
    data = houmer.properties_visited(filter_date)
    result["properties_visited"] = data

    return result


@app.get(
    "/houmers/{houmer_id}/speed_warning",
    name="Houmer Speed Warning",
    summary="Get all moments where a houmer had a speed (km/hr) greater than the given speed, for a day",
    response_description="List where every element is a json with the houmer activity data",
    response_model=ResponseHoumerSpeedWarning,
    responses=speed_warning_responses,
    tags=["Houmer Speed Warning"],
)
async def speed_warnings(
    houmer_id: int,
    speed: float = Body(..., embed=True),
    filter_date: str = Body(..., embed=True),
):
    filter_date = StringToDateValidator(date=filter_date).date
    result = {"houmer_id": houmer_id, "filter_date": filter_date, "speed_filter": speed}

    houmer = Houmer(id=houmer_id)
    data = houmer.speed_warnings(speed, filter_date)

    result["positions_warning"] = data

    return result


@app.post(
    "/properties/{property_id}/insert-markers",
    name="Property Markers",
    summary="Insert latitude and longitude for a property",
    response_description="Message with updated successfully",
    response_model=ResponsePropertyMarkers,
    responses=insert_markers_responses,
    include_in_schema=False,
    tags=["Property Markers"],
)
async def create_property_markers(property_id: int, markers: Markers):
    insert = f"""
    insert into property_markers (property_id, lat, lon)
    values ({property_id}, {markers.lat}, {markers.lon})
    """
    res = BasicQuerys(insert).insert()
    if not res:
        raise HTTPException(
            status_code=501,
            detail="Failed on insert to the database. {property_id} already exist? Maybe..",
        )
    return {
        "message": "New markers updated successfully",
        "property_id": property_id,
        "success": True,
    }


if __name__ == "__main__":
    uvicorn.run("app:app", port=8080, host="0.0.0.0", reload=True)
    # uvicorn.run("app:app", port=8080, reload=True)
