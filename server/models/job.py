from datetime import datetime
import uuid
from typing import Optional, List, Text

import sqlalchemy
from sqlalchemy import String, ForeignKey, Text as saText
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import current_timestamp

from server.models.association_models.job_user import job_user_table
from server.models.base import Base
from server.models.association_models import job_skill_table, job_education_table, job_tag_table


class Job(Base):
    __tablename__ = 'job'

    __disallowed = ('uuid', 'company', 'company_id', 'source', 'source_id', 'date_added', 'skills', 'education', 'tags')

    uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(300), unique=True)
    pay: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    schedule: Mapped[str] = mapped_column(String(20), nullable=True)
    type: Mapped[str] = mapped_column(String(20), nullable=True)  # full time, part, contract, etc
    description: Mapped[Text] = mapped_column(saText(), nullable=True)
    date_added: Mapped[datetime] = mapped_column(default=datetime.now)
    company_id: Mapped[str] = mapped_column(ForeignKey("company.uuid"))
    company: Mapped['Company'] = relationship(back_populates='jobs')
    source_id: Mapped[str] = mapped_column(ForeignKey('source.uuid'))
    source: Mapped['Source'] = relationship(back_populates='jobs')
    user: Mapped[List['User']] = relationship(secondary=job_user_table, back_populates='jobs')
    skills: Mapped[List['Skill']] = relationship(secondary=job_skill_table, back_populates='jobs', lazy='joined')
    education: Mapped[List['Education']] = relationship(secondary=job_education_table, back_populates='jobs', lazy='joined')
    tags: Mapped[List['Tag']] = relationship(secondary=job_tag_table, back_populates='jobs', lazy='joined')

    def __init__(self, title: str, url: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.url = url

        for k, v in kwargs.items():
            assert(k not in self.__class__.__disallowed)
            setattr(self, k, v)

    def update_date_added(self):
        self.date_added = datetime.now()

