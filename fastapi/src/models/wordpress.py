from sqlalchemy import JSON, Boolean, Column, DateTime, Index, String, Text, func
from sqlalchemy.orm import Session, class_mapper, relationship
from sqlalchemy.orm.attributes import instance_dict

from .base_class import BaseClass


class Wordpress(BaseClass):
    __tablename__ = "wordpress"
    blog_url = Column(String)
    blog_name = Column(String(length=200))
    blog_description = Column(Text)
    db_version = Column(String(length=10))
    site_version = Column(String(length=10))
    user_email = Column(String)
    api_credentials = Column(JSON)
    active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    token = relationship("JWT", uselist=False, back_populates="wordpress")  # type: ignore

    __table_args__ = (Index("ix_wordpress_bearer"),)

    # This method courtesy of ChatGPT
    def save(self, db: Session):
        if self.id is not None:
            # get the mapper for the model class
            mapper = class_mapper(type(self))
            # get the names of all columns except for '_sa_instance_state'
            columns = [c.key for c in mapper.columns if c.key != "_sa_instance_state"]
            # get the dictionary of the object's attributes
            values = instance_dict(self)
            # construct the update statement
            db.query(type(self)).filter_by(id=self.id).update(
                {c: values[c] for c in columns}
            )
        else:
            db.add(self)
        db.commit()
        db.refresh(self)
