import uuid
from typing import List

from sqlalchemy import String, Uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column

from server.models.base import Base


class Source(Base):
    __tablename__ = 'source'

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    url: Mapped[str] = mapped_column(String(300), unique=True)
    jobs: Mapped[List["Job"]] = relationship(back_populates='source')

    def __init__(self, name, url):
        self.name = name
        self.url = url

