from models import JWT as JWTModel
from schemas.jwt import JWT, JWTCreate, JWTUpdate
from settings import logger_for

from .general import DAO

logger = logger_for(__name__)


class JWTDAO(DAO[JWTModel, JWT, JWTCreate, JWTUpdate]):  # type: ignore
    pass


jwt_dao = JWTDAO(JWTModel)
