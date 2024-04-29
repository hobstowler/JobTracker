from typing import List

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from server.models.base import Base


class Source(Base):
    __tablename__ = 'source'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    url: Mapped[str] = mapped_column(String(300), unique=True)
    jobs: Mapped[List["Job"]] = relationship(back_populates='source')
