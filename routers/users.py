from fastapi import HTTPException, APIRouter, Depends
from typing import Optional, Annotated
from starlette import status
from sqlalchemy import func

from helpers.utilities import (
    all_passwords_field_provided, get_current_user, access_validator, 
    verify_password, hash_password
)
from database import db_dependency
from models import Users
from routers.validators import UserResponse, UserUpdateRequest

user_dependency = Annotated[dict, Depends(get_current_user)]


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_by_id(db:db_dependency, user:user_dependency):
    access_validator(user, ["user", "admin"])
    query = db.query(Users).filter(Users.user_id == user.get("user_id")).first()

    if query is not None: 
        return query
    else:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
      

@router.put("", status_code=status.HTTP_204_NO_CONTENT)
def update_user( user_request:UserUpdateRequest, db:db_dependency, user:user_dependency):
    access_validator(user, ["user", "admin"])


    all_passwords_field_provided(user_request)

    query = db.query(Users).filter(Users.user_id == user.get("user_id")).first()
    
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        updated_data = user_request.model_dump(exclude_unset=True)
        
        if user_request.current_password is not None:
            if not verify_password(user_request.current_password, query.password):
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")
            if user_request.current_password == user_request.new_password:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Current password can not be the same as new password")

            updated_data.update({
                "password": hash_password(user_request.new_password)
            }) 
            updated_data.pop("current_password")
            updated_data.pop("new_password")


        for key, value in updated_data.items():
            setattr(query, key, value)
        
        db.add(query)
        db.commit()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db:db_dependency, user:user_dependency):
    access_validator(user, ["user", "admin"])

    query = db.query(Users).filter(Users.user_id == user.get("user_id"))
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found")
    else:
        query.delete()
        db.commit()

