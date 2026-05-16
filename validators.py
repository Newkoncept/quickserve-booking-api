from typing import Optional
from pydantic import BaseModel, Field

class ServiceCreateRequest(BaseModel):
    name: str = Field(min_length = 5)
    description: str = Field(min_length = 5, max_length=100)
    price: float = Field(gt=0)
    category: str = Field(min_length = 1)
    is_available: bool = True

    model_config = {
        'extra' : "forbid"
    }

class ServiceUpdateRequest(BaseModel):
    name: Optional[str] = Field(min_length = 5, default=None)
    description: Optional[str] = Field(min_length = 5, max_length=100, default=None)
    price: Optional[float] = Field(gt=0, default=None)
    category: Optional[str] = Field(min_length = 1, default=None)
    is_available: Optional[bool] = None

    model_config = {
        'extra' : "forbid"
    }



class CustomerCreateRequest(BaseModel):
    name: str = Field(min_length = 5)
    email: str = Field(min_length = 5)

    model_config = {
        'extra' : "forbid"
    }
    
class CustomerUpdateRequest(BaseModel):
    name: Optional[str] = Field(min_length = 5, default=None)
    email: Optional[str] = Field(min_length = 5, default=None)

    model_config = {
        'extra' : "forbid"
    }



class BookingCreateRequest(BaseModel):
    customer_id: int = Field(gt=0) 
    service_id: int = Field(gt=0) 
    booking_date: str 
    status: str

    model_config = {
        'extra' : "forbid"
    }

class BookingUpdateRequest(BaseModel):
    status: str

    model_config = {
        'extra' : "forbid"
    }
