import sqlalchemy
from sqlalchemy.orm import Session, class_mapper, declarative_base
from sqlalchemy.orm.attributes import instance_dict

Base = declarative_base()


class BaseClass(Base):
    __abstract__ = True
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, index=True)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.func.now()
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )

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

    # Okay, a lot of this code is coming from ChatGPT
    def __iter__(self):
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                yield key, value


def enum_values(enum_cls):
    return [item.value for item in enum_cls]
