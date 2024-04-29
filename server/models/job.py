from datetime import datetime
from typing import Optional, List, Text

from sqlalchemy import String, ForeignKey, Text as saText
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import current_timestamp

from server.models.base import Base
from server.models.association_models import job_skill_table, job_education_table, job_tag_table


class Job(Base):
    __tablename__ = 'job'

    __disallowed = ('id', 'company', 'company_id', 'source', 'source_id', 'date_added', 'skills', 'education', 'tags')

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(300), unique=True)
    pay: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    schedule: Mapped[str] = mapped_column(String(20), nullable=True)
    type: Mapped[str] = mapped_column(String(20), nullable=True)  # full time, part, contract, etc
    description: Mapped[Text] = mapped_column(saText(), nullable=True)
    date_added: Mapped[datetime] = mapped_column(default=current_timestamp)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped['Company'] = relationship(back_populates='jobs')
    source_id: Mapped[int] = mapped_column(ForeignKey('source.id'))
    source: Mapped['Source'] = relationship(back_populates='jobs')
    skills: Mapped[List['Skill']] = relationship(secondary=job_skill_table, back_populates='jobs')
    education: Mapped[List['Education']] = relationship(secondary=job_education_table, back_populates='jobs')
    tags: Mapped[List['Tag']] = relationship(secondary=job_tag_table, back_populates='jobs')

    def __init__(self, title: str, url: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.url = url

        for k, v in kwargs.items():
            assert(k not in self.__class__.__disallowed)
            setattr(self, k, v)


