from fastapi import HTTPException, Depends
from sqlalchemy import func
from starlette import status
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from dotenv import load_dotenv
import os

from models import Services, Users, Bookings
from routers.validators import JWTToken, UserUpdateRequest

# Load .env file
load_dotenv()



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
expiry_time = timedelta(minutes=20)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


def retrieve_booking(db, 
                    user_id:int | None = None,
                    service_id:int | None = None,
                    booking_date:str | None = None,
                    status_value:str | None = None
                ):
    
    query = db.query(Bookings)

    if (
        user_id is None
        and service_id is None
        and booking_date is None
        and status_value is None
    ):
        return query.all()


    if user_id is not None:
        query = query.filter(Bookings.user_id == user_id)

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


def retrieve_booking_by_id(db, booking_id, user_id):
    query = db.query(Bookings).filter(Bookings.booking_id == booking_id).filter(Bookings.user_id == user_id).first()

    if query is not None:
        return query
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    

def retrieve_full_booking_details_by_id(db, booking_id, user_id,):
    query = db.query(Bookings).filter(Bookings.booking_id == booking_id).filter(Bookings.user_id == user_id).first()

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        user_detail = db.query(Users).filter(Users.user_id == query.user_id).first()
        service_detail = db.query(Services).filter(Services.service_id == query.service_id).first()

        if not user_detail:
            user_detail = {}
        if not service_detail:
            service_detail = {}

        return {
            "booking_id": query.booking_id,
            "service": service_detail,
            "user": user_detail,
            "booking_date": query.booking_date ,
            "status": query.status
        }

        # return {
        #     "booking_id": query.booking_id,
        #     "user": user_detail,
        #     "service": service_detail,
        #     "booking_date": query.booking_date,
        #     "status": query.status
        # }
    

def delete_booking(db, booking_id:int, user_id:int):
    query = db.query(Bookings).filter(Bookings.booking_id == booking_id).filter(Bookings.user_id==user_id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        query.delete()
        db.commit()


def zero_or_value_returner(items):
    if not items:
        return 0
    else:
        return len(items)


def access_validator(user: JWTToken, role: list):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error, unathorized for this route")
    
    if user.get("role") not in role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission role violated")


def all_passwords_field_provided(user_request:UserUpdateRequest):
    current_pwd = user_request.current_password
    new_pwd = user_request.new_password

    if current_pwd is not None and new_pwd is None or new_pwd is not None and current_pwd is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Both password fields needs to be provided")

     

def email_already_exists(email:str, db):
    email_exist = db.query(Users).filter(Users.email == email).first()
    if email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email exists already")


def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(email:str, role:str, user_id: int):
    encode = {
        "sub": email,
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + expiry_time
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(email:str, password:str, db):
    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user

    
def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        user_id:int = payload.get("user_id")
        role:str = payload.get("role")

        if email is None or user_id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
        return {
            "user_id": user_id,
            "role": role
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
        

def create_new_user(user, db, role):
    email_already_exists(user.email, db)
    
    query = Users(**user.model_dump())
    setattr(query, "role", role)
    setattr(query, "password", hash_password(query.password))

    db.add(query)
    db.commit()
    db.refresh(query)

    # delattr(query, "password")

    return query
