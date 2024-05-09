import uuid

from typing import List

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.models.base import Base
from server.models.association_models import job_tag_table


class Tag(Base):
    __tablename__ = 'tag'

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    jobs: Mapped[List['Job']] = relationship(secondary=job_tag_table, back_populates='tags')