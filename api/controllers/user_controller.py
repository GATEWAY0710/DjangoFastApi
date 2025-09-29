from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependency import container
from application.use_case.models.user import CreateUser, ListUserResponse, UserResponse
from fastapi.security import OAuth2PasswordBearer

oauth2_token = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("", response_model=UserResponse)
def create(request: CreateUser, token: str = Depends(oauth2_token)):
    user_service = container.user_service()
    response = user_service.create(request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("", response_model=ListUserResponse)
def list():
    return container.user_service().list()
