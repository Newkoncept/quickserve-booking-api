from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from starlette import status


from schemas import Service, Customer, Booking
from validators import (
    ServiceCreateRequest, ServiceUpdateRequest,
    CustomerCreateRequest, CustomerUpdateRequest,
    BookingCreateRequest, BookingUpdateRequest
)
from utilities import create_new_id, retrieve_detail
from datas import services, bookings, customers


app = FastAPI()



@app.get("/services", status_code=status.HTTP_200_OK)
def get_all_service_or_by_query(
    category:Optional[str] = Query(default=None),
    is_available:bool | None = None,
    price:float | None = None,
):
    
    values_to_be_returned = []

    if category is None and is_available is None and price is None:
        return services

    for service in services:
        if category is not None and service.category.casefold() != category.casefold():
            continue

        if is_available is not None and service.is_available != is_available:
            continue

        if price is not None and service.price != price:
            continue

        values_to_be_returned.append(service)

    if not values_to_be_returned:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No result found"
        )

    return values_to_be_returned

@app.get("/services/{service_id}", status_code=status.HTTP_200_OK)
def get_service_by_id(service_id:int):
    for i in services:
        if i.service_id == service_id:
            return i
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")

@app.post("/services", status_code=status.HTTP_201_CREATED)
def create_service(service:ServiceCreateRequest):
    new_service = Service(service_id = create_new_id(services, "service_id"), **service.model_dump())
    services.append(new_service)
    return new_service

@app.put("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_service(service_id:int, service:ServiceUpdateRequest):
    value_changed = False
    for index, value in enumerate(services):
        if value.service_id == service_id:
            updated_data = service.model_dump(exclude_unset=True)
            for key,value in updated_data.items():
                setattr(services[index], key, value)
            value_changed = True

    if not value_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
        
@app.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id:int):
    value_changed = False
    for index, service in enumerate(services):
        if service.service_id == service_id:
            services.pop(index)

            value_changed = True

    if not value_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")




@app.get("/customers", status_code=status.HTTP_200_OK)
def get_all_customer_or_by_query(
    name: Optional[str] | None = None,
    email: Optional[str] | None = None
):
    values_to_be_returned = []

    if name is None and email is None:
        return customers

    for customer in customers:
        if name is not None and customer.name.casefold() != name.casefold():
            continue

        if email is not None and customer.email.casefold() != email.casefold():
            continue

        values_to_be_returned.append(customer)

    if not values_to_be_returned:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No result found"
        )

    return values_to_be_returned

@app.get("/customers/{customer_id}", status_code=status.HTTP_200_OK)
def get_customer_by_id(customer_id: int):
    for i in customers:
        if i.customer_id == customer_id:
            return i
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
      
@app.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(customer:CustomerCreateRequest):
    new_customer = Customer(
        create_new_id(customers, "customer_id"),
        **customer.model_dump()
        )
    
    customers.append(new_customer)
    return new_customer

@app.put("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_customer(customer_id:int, customer:CustomerUpdateRequest):
    value_changed = False
    for index,value in enumerate(customers):
        if value.customer_id == customer_id:
            updated_data = customer.model_dump(exclude_unset=True)
            for key,value in updated_data.items():
                setattr(customers[index], key, value)
            value_changed = True

    if not value_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int):
    value_changed = False
    for index,value in enumerate(customers):
        if value.customer_id == customer_id:
            customers.pop(index)

            value_changed = True

    if not value_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")




@app.get("/bookings", status_code=status.HTTP_200_OK)
def get_all_booking_or_by_query(
    customer_id:int | None = None,
    service_id:int | None = None,
    booking_date:str | None = None,
    status_value:str | None = None
):
    values_to_be_returned = []

    if (
        customer_id is None
        and service_id is None
        and booking_date is None
        and status_value is None
    ):
        return bookings

    for booking in bookings:
        if customer_id is not None and booking.customer_id != customer_id:
            continue

        if service_id is not None and booking.service_id != service_id:
            continue

        if booking_date is not None and booking.booking_date != booking_date:
            continue

        if status_value is not None and booking.status.casefold() != status_value.casefold():
            continue

        values_to_be_returned.append(booking)

    if not values_to_be_returned:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No result found"
        )

    return values_to_be_returned

@app.get("/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking_by_id(booking_id:int):
    for i in bookings:
        if i.booking_id == booking_id:
            return i
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
 
@app.get("/bookings/full/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking_full_details_by_id(booking_id:int):
    for i in bookings:
        if i.booking_id == booking_id:
            
            customer_detail = retrieve_detail(customers, "customer_id", i.customer_id)
            service_detail = retrieve_detail(services, "service_id", i.service_id)

            return {
                "booking_id": i.booking_id,
                "customer_details": customer_detail,
                "service_details": service_detail,
                "booking_date": i.booking_date,
                "status": i.status
            }
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    
@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking:BookingCreateRequest):
    if retrieve_detail(customers, "customer_id", booking.customer_id) is not None and retrieve_detail(services, "service_id", booking.service_id) is not None:
        new_booking = Booking(booking_id=create_new_id(bookings, "booking_id"), **booking.model_dump())
        bookings.append(new_booking)

        return new_booking
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer or service not found")

@app.put("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_booking(booking_id:int, booking:BookingUpdateRequest):
    value_changed = False
    for index,value in enumerate(bookings):
        if value.booking_id == booking_id:
            updated_data = booking.model_dump(exclude_unset=True)
            for key,value in updated_data.items():
                setattr(bookings[index], key, value)

            value_changed = True

    if not value_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")

@app.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int):
    value_changed = False
    for index,value in enumerate(bookings):
        if value.booking_id == booking_id:
            bookings.pop(index)

            value_changed = True

    if not value_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    