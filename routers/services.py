from fastapi import Depends, HTTPException, Query, APIRouter
from typing import Annotated, Optional
from starlette import status
from sqlalchemy import func


from database import db_dependency
from helpers.utilities import get_current_user
from models import Services
from routers.validators import (
    ServiceCreateRequest, ServiceResponse, ServiceUpdateRequest
)
user_dependency = Annotated[dict, Depends(get_current_user)]


router = APIRouter(
    prefix="/services",
    tags=["services"]
)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[ServiceResponse])
def get_all_service_or_by_query(
    db: db_dependency,
    category:Optional[str] = Query(default=None),
    is_available:bool | None = None,
    price:float | None = None,
):
    query = db.query(Services)

    if category is None and is_available is None and price is None:
        return query.all()

    if category is not None :
        query = query.filter(func.lower(Services.category) == category.casefold())

    if is_available is not None:
        query = query.filter(Services.is_available == is_available)

    if price is not None:
        query = query.filter(Services.price == price)

    services = query.all()

    if not services:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No result found"
        )

    return services


@router.get("/{service_id}", status_code=status.HTTP_200_OK, response_model=ServiceResponse)
def get_service_by_id(service_id:int, db:db_dependency):
    query = db.query(Services).filter(Services.service_id == service_id).first()
    
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    
    return query




