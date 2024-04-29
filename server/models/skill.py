from typing import List

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from server.models.base import Base
from server.models.association_models import job_skill_table


class Skill(Base):
    __tablename__ = 'skill'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    jobs: Mapped[List['Job']] = relationship(secondary=job_skill_table, back_populates='skills')