import uuid
from typing import List, Optional

from sqlalchemy import Uuid, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.models import Base
from server.models.association_models.job_user import job_user_table


class User(Base):
    __tablename__ = 'user'

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    preferred_first_name: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(15))
    prompts: Mapped[List['Prompt']] = relationship(back_populates='user')
    jobs: Mapped[List['Job']] = relationship(secondary=job_user_table, back_populates='user')

    def __init__(self, email, first_name=None, last_name=None, preferred_first_name=None, phone=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.preferred_first_name = preferred_first_name
        self.phone = phone
