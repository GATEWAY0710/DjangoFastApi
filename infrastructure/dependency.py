from dependency_injector import containers, providers
from typing import Callable
from application.persistence.user_repository import UserRepository as DefaultUserRepository
from infrastructure.persistence.user_repository import UserRepository as UserRepository
from application.use_case.user_service import UserService as DefaultUserService
from infrastructure.use_case.user_service import UserService as UserService
import logging
logger = logging.getLogger(__name__)

class Continer(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_repository: Callable[[], DefaultUserRepository] = providers.Factory(
        UserRepository,
        logger=logger
    )

    user_service: Callable[[], DefaultUserService] = providers.Factory(
        UserService,
        logger=logger,
        user_repository=user_repository
    )
     

container = Continer()