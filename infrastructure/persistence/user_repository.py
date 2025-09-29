from typing import List, Optional
from uuid import UUID
 
from sqlalchemy import select
from domain.models import User
from application.persistence.user_repository import UserRepository as DefaultUserRepository
from infrastructure.database import SessionLocal
from sqlalchemy.orm import Session
from logging import Logger

class UserRepository(DefaultUserRepository):
    _logger: Logger
    
    def __init__(self, logger: Logger):
        self._logger = logger
    

    def create(self, user: User) -> Optional[User]:
       with SessionLocal() as session:
            try:
                session.add(user)
                self._logger.info(f"User with id: {user.id} created successfully")
                session.commit()
                session.refresh(user)
                return user
            except Exception as ex:
                self._logger.error(f"An error occured while trying to create user, {ex}")
                return None
            
    def update(self, user: User) -> Optional[User]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(User).where(User.id == user.id)
                )
                
                db_user = session.scalars(statement).one_or_none()
                if db_user is None:
                    self._logger(f"Unable to fine user with id {user.id} to update")
                    return None
                db_user.hash_salt = user.hash_salt
                db_user.password_hash = user.password_hash
                db_user.modified_at = user.modified_at
                db_user.username = user.username
                db_user.modified_by = user.modified_by
                
                session.commit()
                session.refresh(db_user)
                return user
            except Exception as ex:
                self._logger.error(f"Unable to update user, {ex}")
                return None
        
    def get_by_email(self, email: str) -> Optional[User]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(User).where(User.email == email)
                )
                user = session.scalars(statement).one_or_none()
                return user
            except Exception as ex:
                self._logger.error(f"Unable to get user with email {email}, {ex}")
                return None
        
    def get(self, id: UUID) -> Optional[User]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(User).where(User.id == id)
                )
                user = session.scalars(statement).one_or_none()
                return user
            except Exception as ex:
                self._logger.error(f"Unable to get user with id {id}, {ex}")
                return None
        
    
    def list(self) -> List[User]:
        with SessionLocal() as session:
            return session.scalars(select(User)).all()
            
        