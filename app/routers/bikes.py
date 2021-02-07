__author__ = 'sajive'
from typing import Optional
from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from ..dependencies import get_token_header


class BikeIn(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    status: str


class BikeOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    status: str


app = APIRouter(
    prefix="/bikes",
    tags=["bikes"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@app.post("/")
async def create_item(bike: BikeIn):
    return bike


bike = [BikeOut(id=1, name="BMW", price=400.5, status="booked"),
        BikeOut(id=2, name="Yamaha", price=200.0, status="available"),
        BikeOut(id=3, name="Suzuki", price=100.5, status="service"),
        ]


@app.get("/")
async def get_bikes():
    return bike


@app.get("/bikes/{bike_id}", response_model=BikeOut,
         response_model_exclude_unset=True)
async def get_bike_id(bike_id: int):
    # return {"bike_id": bike_id, "info": bike[bike_id]}
    # return {"bike id": bike[bike_id]} # works if it matches the response model

    bikeFound = bike[bike_id]
    bikeFound.id = 200

    return bike[bike_id]
