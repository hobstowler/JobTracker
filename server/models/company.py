import uuid
from typing import List

import uuid as uuid
from sqlalchemy import String, Uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column

from server.models.base import Base


class Company(Base):
    __tablename__ = 'company'

    __disallowed = ('id')

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(100), nullable=True)
    jobs: Mapped[List["Job"]] = relationship(back_populates='company')

    def __init__(self, name: str, **kwargs):
        self.name = name

        for k, v in kwargs.items():
            assert(k not in self.__class__.__disallowed)
            setattr(self, k, v)
