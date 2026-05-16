from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from starlette import status
from sqlalchemy import func

import models
from database import engine, db_dependency
from models import Services, Customers, Bookings
from validators import (
    ServiceCreateRequest, ServiceUpdateRequest,
    CustomerCreateRequest, CustomerUpdateRequest,
    BookingCreateRequest, BookingUpdateRequest
)
from utilities import retrieve_details

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/services", status_code=status.HTTP_200_OK)
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

@app.get("/services/{service_id}", status_code=status.HTTP_200_OK)
def get_service_by_id(service_id:int, db:db_dependency):
    query = db.query(Services).filter(Services.service_id == service_id).first()
    
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    
    return query

@app.post("/services", status_code=status.HTTP_201_CREATED)
def create_service(service:ServiceCreateRequest, db:db_dependency):
    query = Services(**service.model_dump())
    
    db.add(query)
    db.commit()
    db.refresh(query)

    return query

@app.put("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_service(service_id:int, service:ServiceUpdateRequest, db:db_dependency):
    query = db.query(Services).filter(Services.service_id == service_id).first()
    
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        updated_data = service.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(query, key, value)
        
        db.add(query)
        db.commit()
     
@app.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id:int, db:db_dependency):
    query = db.query(Services).filter(Services.service_id == service_id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        query.delete()
        db.commit()




@app.get("/customers", status_code=status.HTTP_200_OK)
def get_all_customer_or_by_query(
    db:db_dependency,
    name: Optional[str] | None = None,
    email: Optional[str] | None = None
):
    query = db.query(Customers)

    if name is None and email is None:
        return query.all()

    if name is not None :
        query = query.filter(func.lower(Customers.name) == name.casefold())

    if email is not None:
        query = query.filter(func.lower(Customers.email) == email.casefold())

    query = query.all()

    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No result found"
        )

    return query

@app.get("/customers/{customer_id}", status_code=status.HTTP_200_OK)
def get_customer_by_id(customer_id: int, db:db_dependency):
    query = db.query(Customers).filter(Customers.customer_id == customer_id).first()

    if query is not None: 
        return query
    else:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
      
@app.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(customer:CustomerCreateRequest, db:db_dependency):
    query = Customers(**customer.model_dump())
    
    db.add(query)
    db.commit()
    db.refresh(query)

    return query

@app.put("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_customer(customer_id:int, customer:CustomerUpdateRequest, db:db_dependency):
    query = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        updated_data = customer.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(query, key, value)
        
        db.add(query)
        db.commit()

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db:db_dependency):
    query = db.query(Customers).filter(Customers.customer_id == customer_id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        query.delete()
        db.commit()




@app.get("/bookings", status_code=status.HTTP_200_OK)
def get_all_booking_or_by_query(
    db:db_dependency,
    customer_id:int | None = None,
    service_id:int | None = None,
    booking_date:str | None = None,
    status_value:str | None = None
):
    
    query = db.query(Bookings)

    if (
        customer_id is None
        and service_id is None
        and booking_date is None
        and status_value is None
    ):
        return query.all()


    if customer_id is not None:
        query = query.filter(Bookings.customer_id == customer_id)

    if service_id is not None:
        query = query.filter(Bookings.service_id == service_id)

    if booking_date is not None:
        query = query.filter(Bookings.booking_date == booking_date)

    if status_value is not None:
        query = query.filter(func.lower(Bookings.status) == status_value.casefold())

    query = query.all()

    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No result found"
        )

    return query

@app.get("/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking_by_id(booking_id:int, db:db_dependency):
    query = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
    if query is not None:
        return query
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
 
@app.get("/bookings/full/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking_full_details_by_id(booking_id:int, db:db_dependency):
    query = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        customer_detail = retrieve_details(db, Customers, "customer_id", query.customer_id)
        service_detail = retrieve_details(db, Services, "service_id", query.service_id)

        return {
            "booking_id": query.booking_id,
            "customer_details": customer_detail,
            "service_details": service_detail,
            "booking_date": query.booking_date,
            "status": query.status
        }
    
@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking:BookingCreateRequest, db:db_dependency):
    if retrieve_details(db, Customers, "customer_id", booking.customer_id) is not None and retrieve_details(db, Services, "service_id", booking.service_id) is not None:
        
        query = Bookings(**booking.model_dump())
    
        db.add(query)
        db.commit()
        db.refresh(query)

        return query

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer or service not found")

@app.put("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_booking(booking_id:int, booking:BookingUpdateRequest, db:db_dependency):
    query = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
    
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        updated_data = booking.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(query, key, value)
        
        db.add(query)
        db.commit()

@app.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db:db_dependency):
    query = db.query(Bookings).filter(Bookings.booking_id == booking_id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        query.delete()
        db.commit()
    