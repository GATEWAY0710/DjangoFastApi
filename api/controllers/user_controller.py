from fastapi import APIRouter, HTTPException
from infrastructure.dependency import container
from application.use_case.models.user import CreateUser, UserResponse

router = APIRouter()

@router.post("", response_model=UserResponse)
def create(request: CreateUser):
    user_service = container.user_service()
    response = user_service.create(request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response