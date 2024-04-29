from sqlalchemy import Table, Column, ForeignKey

from server.models.base import Base

job_education_table = Table(
    'job_education',
    Base.metadata,
    Column('job_id', ForeignKey('job.id'), primary_key=True),
    Column('education_id', ForeignKey('education.id'), primary_key=True)
)