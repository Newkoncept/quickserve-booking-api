from fastapi import HTTPException, APIRouter, Depends
from typing import Optional, Annotated
from starlette import status
from sqlalchemy import func

from helpers.utilities import (
    access_validator, create_new_user, delete_booking, 
    get_current_user, retrieve_booking, retrieve_booking_by_id, retrieve_full_booking_details_by_id, zero_or_value_returner,
)
from database import db_dependency
from models import Users, Services, Bookings
from routers.validators import (
    BookingUpdateRequest, UserCreateRequest,
    ServiceCreateRequest, ServiceUpdateRequest, 

    UserResponse, ServiceResponse,
    
)
user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.post("/user/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_admin_user(user:UserCreateRequest, db:db_dependency):
    return create_new_user(user, db, "admin")


@router.post("/services/create_service", status_code=status.HTTP_201_CREATED, response_model=ServiceResponse)
def create_service(service:ServiceCreateRequest, db:db_dependency, user:user_dependency):
    access_validator(user, ["admin"])
    query = Services(**service.model_dump())
    
    db.add(query)
    db.commit()
    db.refresh(query)

    return query


@router.put("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_service(service_id:int, service:ServiceUpdateRequest, db:db_dependency, user:user_dependency):
    access_validator(user, ["admin"])

    query = db.query(Services).filter(Services.service_id == service_id).first()
    
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        updated_data = service.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(query, key, value)
        
        db.add(query)
        db.commit()


@router.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id:int, db:db_dependency, user:user_dependency):
    access_validator(user, ["admin"])

    query = db.query(Services).filter(Services.service_id == service_id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        query.delete()
        db.commit()


@router.put("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_booking(booking_id:int, booking:BookingUpdateRequest, db:db_dependency, user:user_dependency):
    access_validator(user, ["admin"])
    
    query = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
    
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        updated_data = booking.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(query, key, value)
        
        db.add(query)
        db.commit()


@router.get("", status_code=status.HTTP_200_OK)
def get_all_stats(user:user_dependency, db:db_dependency):
    access_validator(user, ["admin"])

    return {
        "Total services": zero_or_value_returner(db.query(Services).all()),
        "Total bookings": zero_or_value_returner(db.query(Bookings).all()),
        "Total users": zero_or_value_returner(db.query(Users).all())
    }


@router.get("/user", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def get_all_users_or_by_query(
    user: user_dependency,
    db:db_dependency,
    name: Optional[str] | None = None,
    email: Optional[str] | None = None
):
    access_validator(user, ["admin"])
    
    query = db.query(Users)

    if name is None and email is None:
        return query.all()

    if name is not None :
        query = query.filter(func.lower(Users.name) == name.casefold())

    if email is not None:
        query = query.filter(func.lower(Users.email) == email.casefold())

    query = query.all()

    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No result found"
        )

    return query


@router.get("/booking", status_code=status.HTTP_200_OK)
def get_all_bookings_or_by_query(
    db:db_dependency,
    user:user_dependency,
    user_id:int | None = None,
    service_id:int | None = None,
    booking_date:str | None = None,
    status_value:str | None = None
):
    access_validator(user, ["admin"])
    return retrieve_booking(db, user_id, service_id, booking_date, status_value)

@router.get("/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking_by_id(booking_id:int, user_id:int, db:db_dependency, user:user_dependency):
    access_validator(user, ["admin"])
    return retrieve_booking_by_id(db, booking_id, user_id)

@router.get("/full/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking_full_details_by_id(booking_id:int, user_id:int, db:db_dependency, user:user_dependency):
    access_validator(user, ["admin"])
    return retrieve_full_booking_details_by_id(db, booking_id, user_id)
 
@router.delete("/booking/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking_from_DB(booking_id: int, user_id:int, db:db_dependency, user:user_dependency):
    access_validator(user, ["admin"])
    delete_booking(db, booking_id, user_id)