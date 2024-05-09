from typing import Type, Optional

from sqlalchemy.orm import Session

from server.models import Search
from server.repositories.base_repository import BaseRepository, with_session, DEFAULT_LIMIT


class SearchRepository(BaseRepository):
    @with_session
    def add(self, session: Session, search: Search) -> str:
        session.add(search)
        session.flush()

        return search.uuid

    @with_session
    def get(self, session: Session, limit=DEFAULT_LIMIT, offset: int = 0) -> list[Type[Search]]:
        searches = session.query(Search).limit(limit).offset(offset).all()

        return searches

    @with_session
    def get_by_id(self, session: Session, search_uuid: str) -> Optional[Search]:
        search = session.query(Search).where(Search.uuid == search_uuid).first()

        return search

    # @with_session
    # def get_by_user_id(self, session: Session, search_uuid: str) -> Optional[Search]:
    #     search = session.query(Search).where(Search.uuid == search_uuid).first()
    #
    #     return search

    @with_session
    def update(self, session: Session, search: Search) -> None:
        valid_attr = {k: v for (k, v) in search.__dict__.items() if k not in ['_sa_instance_state', 'uuid']}
        print(valid_attr)

        session.query(Search).where(Search.uuid == search.uuid).update(valid_attr)

    @with_session
    def delete(self, session: Session, search_uuid: str) -> None:
        search_to_delete = session.query(Search).where(Search.uuid == search_uuid).first()

        if search_to_delete:
            session.delete(search_to_delete)
