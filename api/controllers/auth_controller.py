from application.use_case.models.auth import TokenResponse
from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.dependency import container
router = APIRouter()
@router.post("/token", response_model=TokenResponse)
def token(email: str, password: str):
    user_service = container.user_service()
    response = user_service.authenticate(email, password)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    
    user = container.user_service().get_by_email(email).user