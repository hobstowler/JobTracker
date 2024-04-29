from sqlalchemy import Table, Column, ForeignKey

from server.models.base import Base

job_tag_table = Table(
    'job_tag',
    Base.metadata,
    Column('job_id', ForeignKey('job.id'), primary_key=True),
    Column('tag_id', ForeignKey('tag.id'), primary_key=True)
)
