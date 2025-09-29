import uuid
from domain.models import User
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.user import CreateUser, ListUserResponse, UserResponse
from application.use_case.user_service import UserService as DefaultUserService
from application.persistence.user_repository import UserRepository
from logging import Logger
from infrastructure.helpers.hashing import HashingService


class UserService(DefaultUserService):
    _logger: Logger
    _user_repository: UserRepository
    
    def __init__(self, logger: Logger, user_repository: UserRepository):
        self._logger = logger
        self._user_repository = user_repository
        
    def create(self, user: CreateUser) -> BaseResponse:
        self._logger.info(f"Creating user with email {user.email}")
        
        ## check if provided email already exists
        existing_user = self._user_repository.get_by_email(email=user.email)
        if existing_user:
            self._logger.warning(f"User with email {user.email} already exits")
            response = BaseResponse(status=False, message=f"User with email {user.email} already exits")
            response._status_code = 400
            return response
        
        ## validate password
        if not user.validate_password():
            self._logger.warning(f"Provided password dose not match")
            response = BaseResponse(status=False, message=f"Provided password dose not match")
            response._status_code = 400
            return response
        
        ## hash password
        hash_salt, password_hash = HashingService().hash_password(user.password)
        
        if user.username is None:
            user.username = user.email
        
        db_user = User(email=user.email, hash_salt=hash_salt, password_hash=password_hash, username=user.username)
        db_user = self._user_repository.create(db_user)
        if not db_user:
            self._logger.error("An error occured while trying to create user")
            response = BaseResponse(status=False, message="An error occured while trying to create user")
            response._status_code = 500
            return response
        
        self._logger.info(f"User with email {user.email} created successfully")
        response = UserResponse(status=True, id=db_user.id, email=db_user.email, username=db_user.username)
        response._status_code = 201
        return response
        
    def list(self) -> BaseResponse:
        self._logger.info("Listing users")
        users = self._user_repository.list()
        user_responses = []
        for user in users:
            user_responses.append(UserResponse(
                status=True,
                id=user.id,
                email=user.email,
                username=user.username
            ))
        response = ListUserResponse(status=True, message="Users listed successfully", users=user_responses)
        response.users = user_responses
        response._status_code = 200
        return response
    
    def authenticate(self, email, password):
        user = self._user_repository.get_by_email(email=email)
        if not user:
            response = BaseResponse(status=False, message="Invalid email or password")
            response._status_code = 401
            return response
        
        if not HashingService().verify_password(password, user.hash_salt, user.password_hash):
            response = BaseResponse(status=False, message="Invalid email or password")
            response._status_code = 401
            return response
        
        return BaseResponse(status=True, message="User authenticated successfully")
        
        
        
        
        