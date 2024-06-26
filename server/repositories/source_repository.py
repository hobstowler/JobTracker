from typing import Optional, Type

from sqlalchemy.orm import Session

from server.models import Source
from server.repositories.base_repository import BaseRepository, with_session, DEFAULT_LIMIT


class SourceRepository(BaseRepository):
    @with_session
    def add(self, session: Session, source: Source) -> str:
        session.add(source)
        session.flush()

        return source.uuid

    @with_session
    def get(self, session: Session, limit=DEFAULT_LIMIT, offset: int = 0) -> list[Type[Source]]:
        sources = session.query(Source).limit(limit).offset(offset).all()

        return sources

    @with_session
    def get_by_id(self, session: Session, source_uuid: str) -> Optional[Source]:
        source = session.query(Source).where(Source.uuid == source_uuid).first()

        return source

    @with_session
    def get_by_name(self, session: Session, source_name: str) -> Optional[Source]:
        source = session.query(Source).where(Source.name == source_name).first()

        return source

    @with_session
    def update(self, session: Session, source: Source) -> None:
        valid_attr = {k: v for (k, v) in source.__dict__.items() if k not in ['_sa_instance_state', 'uuid']}

        session.query(Source).where(Source.uuid == source.uuid).update(valid_attr)

    @with_session
    def delete(self, session: Session, source_uuid: str) -> None:
        source_to_delete = session.query(Source).where(Source.uuid == source_uuid).first()

        if source_to_delete:
            session.delete(source_to_delete)


# source = Source('indeed', 'https://www.indeed.com')
# source_repo = SourceRepository()
# source_repo.add(source)
