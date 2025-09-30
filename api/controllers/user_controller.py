from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependency import container
from application.use_case.models.user import CreateUser, ListUserResponse, UserResponse
from fastapi.security import OAuth2PasswordBearer
from api.token import allowed_roles, get_current_user
from typing import Annotated
from application.use_case.models.auth import TokenData

router = APIRouter()

@router.post("", response_model=UserResponse)
def create(request: CreateUser):
    user_service = container.user_service()
    response = user_service.create(request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("", response_model=ListUserResponse)
def list(current_user: Annotated[TokenData, Depends(allowed_roles(["admin"]))]):
    email = current_user.email
    
    return container.user_service().list()
