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



class UserCreateRequest(BaseModel):
    name: str = Field(min_length = 5)
    email: str = Field(min_length = 5)
    password: str = Field(min_length = 5)
    # role: str = Field(min_length = 3)

    model_config = {
        'extra' : "forbid"
    }
    
class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(min_length = 5, default=None)
    # email: Optional[str] = Field(min_length = 5, default=None)
    current_password: Optional[str] = Field(min_length = 5, default=None)
    new_password: Optional[str] = Field(min_length = 5, default=None)
    # role: Optional[str] = Field(min_length = 3, default=None)

    model_config = {
        'extra' : "forbid"
    }



class BookingCreateRequest(BaseModel):
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


class JWTToken(BaseModel):
    user_id: int
    role: str


class UserResponse(BaseModel):
    user_id: int | None = None
    email: str | None = None
    name: str | None = None
    role: str | None = None

    model_config = {
        "from_attributes": True
    } 


class ServiceResponse(BaseModel):
    service_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None
    is_available: bool | None = None

    model_config = {
        "from_attributes": True
    }


class BookingResponse(BaseModel):
    user_id: int
    service_id: int
    status: str
    booking_date: str
    booking_id: int


class BookingFullResponse(BaseModel):
    booking_id: int
    service: ServiceResponse
    user: UserResponse
    booking_date: str 
    status: str