from fastapi_restful.api_model import APIModel
import typing as t
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa


Base = declarative_base()


class NotesOrm(Base):
    __tablename__ = "notesitem"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    content = sa.Column(sa.String, nullable=False)


class NoteCreate(APIModel):
    title: t.Optional[str]
    content: str

class NoteCreateOut(NoteCreate):
    id: int

    @classmethod
    def from_orm_list(cls, obj, count_title):
        instance = cls.from_orm(obj)
        if instance.title is None:
            instance.title = instance.content[:count_title]
        return instance