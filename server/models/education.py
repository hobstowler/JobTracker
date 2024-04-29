from typing import List

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from server.models.base import Base
from server.models.association_models import job_education_table


class Education(Base):
    __tablename__ = 'education'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    jobs: Mapped[List['Job']] = relationship(secondary=job_education_table, back_populates='education')
