# Code courtesy of ChatGPT
from typing import Any, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from settings import logger_for
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Query, Session

logger = logger_for(__name__)

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class DAO(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def _get_base_query(self, db: Session) -> Query:
        return db.query(self.model)

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return self._get_base_query(db).filter(self.model.id == id).first()  # type: ignore

    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        return (
            self._get_base_query(db).filter(getattr(self.model, field) == value).first()
        )

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self._get_base_query(db).offset(skip).limit(limit).all()

    def create(self, db: Session, schema: CreateSchemaType) -> ModelType:
        db_obj = self.model(**schema.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, schema: UpdateSchemaType) -> ModelType:
        db_obj = self.get(db, id)
        if db_obj:
            for key, value in schema.dict().items():
                if value is not None:
                    setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        else:
            raise ValueError(f"No object of {self.model} with id {id} exists")

    def update_by_field(
        self, db: Session, field: str, value: str, schema: UpdateSchemaType
    ) -> List[ModelType]:
        db_objs = (
            self._get_base_query(db).filter(getattr(self.model, field) == value).all()
        )
        for db_obj in db_objs:
            for key, updated_value in schema.dict().items():
                if updated_value is not None:
                    setattr(db_obj, key, updated_value)
        db.commit()
        return db_objs

    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    def delete_by_field(self, db: Session, field: str, value: str) -> List[ModelType]:
        db_objs = (
            self._get_base_query(db).filter(getattr(self.model, field) == value).all()
        )
        for db_obj in db_objs:
            db.delete(db_obj)
        db.commit()
        return db_objs
