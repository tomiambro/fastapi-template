import sqlalchemy
from sqlalchemy.orm import relationship

from .base_class import BaseClass


class JWT(BaseClass):
    __tablename__ = "jwt"
    token = sqlalchemy.Column(sqlalchemy.String, unique=True)
    expiration_date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.now()
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )
    wordpress_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("wordpress.id")
    )
    wordpress = relationship("Wordpress", back_populates="token")  # type: ignore

    def __str__(self):
        return (
            f"<models.JWT(id={self.id}, token='{self.token}', expiration_date='{self.expiration_date}', wordpress_id='{self.wordpress_id}', "
            f"blog={self.blog}, created_at={self.created_at}, updated_at={self.updated_at})>"
        )
