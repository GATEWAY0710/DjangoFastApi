from application.use_case.models.auth import TokenResponse
from fastapi import APIRouter, Depends, HTTPException, status, Body
from application.use_case.models.user import UserResponse
from infrastructure.dependency import container
from api.token import create_token


router = APIRouter()
@router.post("/token", response_model=TokenResponse)
def token(email: str = Body(), password: str = Body()):
    user_service = container.user_service()
    response = user_service.authenticate(email, password)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    
    response: UserResponse = container.user_service().get_by_email(email)
    
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    
    email = response.email
    user_id = response.id
    username = response.username
    
    data = {
        "sub": email,
        "user_id": str(user_id),
        "username": username,
        "roles" : ["user"]
    }
    
    access_token, refresh_token, expire = create_token(data, expires_delta=None)
    
    return TokenResponse(
        status=True,
        message="Token generated successfully",
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=int(expire.timestamp())
    )