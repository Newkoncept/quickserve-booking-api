from fastapi import HTTPException, APIRouter, Depends
from typing import Annotated
from starlette import status
from sqlalchemy import func

from helpers.utilities import (
    delete_booking, get_current_user, 
    retrieve_booking, retrieve_booking_by_id, 
    access_validator, retrieve_full_booking_details_by_id
)
from database import db_dependency
from models import Services, Users, Bookings
from routers.validators import (
    BookingCreateRequest,
    BookingFullResponse,
    BookingResponse
)

user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[BookingResponse])
def get_all_booking_or_by_query(
    db:db_dependency,
    user:user_dependency,
    service_id:int | None = None,
    booking_date:str | None = None,
    status_value:str | None = None
):
    access_validator(user, ["user"])    
    return retrieve_booking(db, user.get("user_id"), service_id, booking_date, status_value)
    

@router.get("/{booking_id}", status_code=status.HTTP_200_OK, response_model=BookingResponse)
def get_booking_by_id(booking_id:int, db:db_dependency, user:user_dependency):
    access_validator(user, ["user"])
    return retrieve_booking_by_id(db, booking_id, user.get("user_id"))
    
 
@router.get("/full/{booking_id}", status_code=status.HTTP_200_OK, response_model=BookingFullResponse)
def get_booking_full_details_by_id(booking_id:int, db:db_dependency, user:user_dependency):
    return retrieve_full_booking_details_by_id(db, booking_id, user.get("user_id"))


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookingResponse)
def create_booking(booking:BookingCreateRequest, db:db_dependency, user:user_dependency):
    access_validator(user, ["user"])

    requested_service = db.query(Services).filter(Services.service_id == booking.service_id).first()
    if not requested_service or not requested_service.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service not found/available")
    
    query = Bookings(**booking.model_dump())
    setattr(query, "user_id", user.get("user_id"))


    db.add(query)
    db.commit()
    db.refresh(query)

    return query


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking_from_DB(booking_id: int, db:db_dependency, user:user_dependency):
    access_validator(user, ["user"])
    delete_booking(db, booking_id, user.get("user_id"))

