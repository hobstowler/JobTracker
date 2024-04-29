from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class Search(Base):
    __tablename__ = 'search'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    title: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(50), nullable=True)
    lookback_days: Mapped[int]