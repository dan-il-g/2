from fastapi import Depends, HTTPException
from fastapi_restful.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from fastapi_restful.cbv import cbv

from notes.database import NoteCreate, NoteCreateOut, NotesOrm
from notes.dependencies import get_db
import typing as t

count_title_symbols = 10
router = InferringRouter()

@cbv(router)
class ItemCBV:
    session: Session = Depends(get_db)

    @router.post("/notes")
    def create_item(self, item: NoteCreate) -> NoteCreateOut:
        """
        Создание заметки
        :param item:
        :return:
        """
        item_orm = NotesOrm(
            title=item.title,
            content=item.content,
        )
        self.session.add(item_orm)
        self.session.commit()
        return NoteCreateOut.from_orm(item_orm)

    @router.get("/notes/{id}")
    def get_item(self, id: int) -> NoteCreateOut:
        """
        Получить заметку по ID
        :return:
        """
        result = self.session.query(NotesOrm).filter(NotesOrm.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Notes not found")
        return NoteCreateOut.from_orm_list(result, count_title_symbols)

    @router.put("/notes/{id}")
    def update_item(self, id: int, item: NoteCreate) -> NoteCreateOut:
        """
        Получить заметку по ID
        :return:
        """
        result = self.session.query(NotesOrm).filter(NotesOrm.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Notes not found")
        # Update
        result.title = item.title
        result.content = item.content
        self.session.add(result)
        self.session.commit()
        return NoteCreateOut.from_orm(result)

    @router.get("/notes")
    def get_item_by_query_or_all(self, query: t.Optional[str] = None) -> t.List[NoteCreateOut]:
        """
        Получить заметку по Query или получить ВСЕ заметки
        :return:
        """
        if query is None:
            results = self.session.query(NotesOrm)
        else:
            results = self.session.query(NotesOrm).filter(
                (NotesOrm.title.contains(query)) |
                (NotesOrm.content.contains(query))
            )

        return [NoteCreateOut.from_orm_list(x, count_title_symbols) for x in results]

    @router.delete("/notes/{id}")
    def update_item(self, id: int) -> NoteCreateOut:
        """
        Получить заметку по ID
        :return:
        """
        result = self.session.query(NotesOrm).filter(NotesOrm.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Notes not found")
        # Update
        dropped = NoteCreateOut.from_orm(result)
        self.session.delete(result)
        self.session.commit()
        return dropped

