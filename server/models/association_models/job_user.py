from sqlalchemy import Table, Column, ForeignKey

from server.models.base import Base

job_user_table = Table(
    'job_user',
    Base.metadata,
    Column('job_id', ForeignKey('job.uuid'), primary_key=True),
    Column('user_id', ForeignKey('user.uuid'), primary_key=True)
)
