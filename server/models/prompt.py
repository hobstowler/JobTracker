import uuid

from sqlalchemy import Uuid, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.models import Base


class Prompt(Base):
    __tablename__ = 'prompt'

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    prompt_string: Mapped[str] = mapped_column(String(1000))
    prompt_type: Mapped[str] = mapped_column(String(20), default='string')
    response: Mapped[str] = mapped_column(String(100), default='')
    source_id: Mapped[str] = mapped_column(ForeignKey('source.uuid'))
    source: Mapped['Source'] = relationship()
    user_id: Mapped[str] = mapped_column(ForeignKey('user.uuid'))
    user: Mapped['User'] = relationship()

