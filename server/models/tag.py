from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.models.base import Base
from server.models.association_models import job_tag_table


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    jobs: Mapped[List['Job']] = relationship(secondary=job_tag_table, back_populates='tags')