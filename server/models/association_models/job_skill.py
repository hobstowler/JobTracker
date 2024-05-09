from sqlalchemy import Table, Column, ForeignKey

from server.models.base import Base

job_skill_table = Table(
    'job_skill',
    Base.metadata,
    Column('job_id', ForeignKey('job.uuid'), primary_key=True),
    Column('skill_id', ForeignKey('skill.uuid'), primary_key=True)
)