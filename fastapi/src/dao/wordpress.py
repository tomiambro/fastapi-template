from models import Wordpress as WordpressModel
from schemas.wordpress import Wordpress, WordpressCreate, WordpressUpdate
from settings import logger_for
from sqlalchemy.orm import Session

from .general import DAO

logger = logger_for(__name__)


class WordpressDAO(DAO[WordpressModel, Wordpress, WordpressCreate, WordpressUpdate]):  # type: ignore
    def create(self, db: Session, obj_in: WordpressCreate) -> WordpressModel:
        obj_in_dict = obj_in.dict(exclude={"wordpress_api_credentials"})

        db_obj = self.model(**obj_in_dict)
        db.add(db_obj)
        db.commit()

        db.refresh(db_obj)
        return db_obj


wordpress_dao = WordpressDAO(WordpressModel)

# Examples
# user = user_dao.get(db, user_id)
# user_by_email = user_dao.get_by_field(db, "email", email)
# users = user_dao.get_all(db, skip, limit)
# new_user = user_dao.create(db, user_create_schema)

# # Update a user by ID
# updated_user = user_dao.update(db, user_id, user_update_schema)

# # Update all users with a specific email
# updated_users = user_dao.update_by_field(db, "email", email, user_update_schema)

# # Delete a user by ID
# deleted_user = user_dao.delete(db, user_id)

# # Delete all users with a specific email
# deleted_users = user_dao.delete_by_field(db, "email", email)
