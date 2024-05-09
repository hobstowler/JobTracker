from typing import List

import uuid
from sqlalchemy import String, Uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column

from server.models.base import Base
from server.models.association_models import job_education_table


class Education(Base):
    __tablename__ = 'education'

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    jobs: Mapped[List['Job']] = relationship(secondary=job_education_table, back_populates='education')
