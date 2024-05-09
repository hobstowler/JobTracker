import uuid
from typing import List

from sqlalchemy import String, Uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column

from server.models.base import Base
from server.models.association_models import job_skill_table


class Skill(Base):
    __tablename__ = 'skill'

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    jobs: Mapped[List['Job']] = relationship(secondary=job_skill_table, back_populates='skills')
