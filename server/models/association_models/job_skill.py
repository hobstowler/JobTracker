from sqlalchemy import Table, Column, ForeignKey

from server.models.base import Base

job_skill_table = Table(
    'job_skill',
    Base.metadata,
    Column('job_id', ForeignKey('job.id'), primary_key=True),
    Column('skill_id', ForeignKey('skill.id'), primary_key=True)
)