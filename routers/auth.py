from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm


from database import db_dependency
from models import Users
from routers.validators import UserCreateRequest, UserUpdateRequest, UserResponse
from helpers.utilities import (
    create_new_user, email_already_exists, hash_password, 
    authenticate_user, create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

USER_ROLE = "user"



@router.post("/login")
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")
    
    token = create_access_token(user.email, user.role, user.user_id)
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user:UserCreateRequest, db:db_dependency):
    return create_new_user(user, db, "user")

