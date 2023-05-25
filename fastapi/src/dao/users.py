from models import User as UserModel
from schemas import User, UserCreate, UserUpdate
from settings import logger_for

from .general import DAO

logger = logger_for(__name__)


class UserDAO(DAO[UserModel, User, UserCreate, UserUpdate]):  # type: ignore
    pass


user_dao = UserDAO(UserModel)
