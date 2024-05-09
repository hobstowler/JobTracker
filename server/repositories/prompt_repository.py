from typing import Optional, Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from server.models import Prompt
from server.repositories.base_repository import BaseRepository, with_session, DEFAULT_LIMIT


class PromptRepository(BaseRepository):
    @with_session
    def add(self, session: Session, prompt: Prompt) -> str:
        session.add(prompt)
        session.flush()

        return prompt.uuid

    @with_session
    def get_by_user_id_and_source_id(self, session: Session, user_uuid: str, source_uuid: str) -> list[Type[Prompt]]:
        prompts = session.query(Prompt).where(
            Prompt.user_id == user_uuid and
            Prompt.source_id == source_uuid
        ).all()

        return prompts

    @with_session
    def get_by_id(self, session: Session, prompt_uuid: str) -> Optional[Prompt]:
        prompt = session.query(Prompt).where(Prompt.uuid == prompt_uuid).first()

        return prompt

    @with_session
    def update(self, session: Session, prompt: Prompt) -> None:
        valid_attr = {k: v for (k, v) in prompt.__dict__.items() if k not in ['_sa_instance_state', 'uuid']}

        session.query(Prompt).where(Prompt.uuid == prompt.uuid).update(valid_attr)

    @with_session
    def delete(self, session: Session, prompt_uuid: str) -> None:
        prompt_to_delete = session.query(Prompt).where(Prompt.uuid == prompt_uuid).first()

        if prompt_to_delete:
            session.delete(prompt_to_delete)
