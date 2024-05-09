import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class Search(Base):
    __tablename__ = 'search'

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    title: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(50), nullable=True)
    lookback_days: Mapped[int] = mapped_column(nullable=True)
    remote: Mapped[bool] = mapped_column(nullable=True)

    def __init__(self, title: str, location: str, remote: bool = None, lookback_days: int = None):
        self.title = title
        self.location = location
        self.remote = remote
        self.lookback_days = lookback_days
