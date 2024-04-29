from typing import Optional, Type

from sqlalchemy.orm import Session

from server.models import Job
from server.repositories.base_repository import BaseRepository, with_session, DEFAULT_LIMIT


class JobRepository(BaseRepository):
    @with_session
    def add(self, session: Session, job: Job) -> int:
        session.add(job)
        session.flush()

        return job.id

    @with_session
    def get(self, session: Session, limit=DEFAULT_LIMIT, offset: int = 0) -> list[Type[Job]]:
        jobs = session.query(Job).limit(limit).offset(offset).all()

        return jobs

    @with_session
    def get_by_id(self, session: Session, job_id: int) -> Optional[Job]:
        job = session.query(Job).where(Job.id == job_id).first()

        return job

    @with_session
    def update(self, session: Session, job: Job) -> None:
        valid_attr = {k: v for (k, v) in job.__dict__.items() if k not in ['_sa_instance_state', 'id', 'date_added']}

        session.query(Job).where(Job.id == job.id).update(valid_attr)

    @with_session
    def delete(self, session: Session, job_id: int) -> None:
        job_to_delete = session.query(Job).where(Job.id == job_id).first()

        if job_to_delete:
            session.delete(job_to_delete)


# job_repo = JobRepository()
# company_repo = CompanyRepository()
# source_repo = SourceRepository()
#
# # company = Company(name='Oracle')
# # print(company_repo.add(company))
# company = company_repo.get_by_id(1)
#
# # source = Source(name='indeed', url='https://www.indeed.com')
# # print(source_repo.add(source))
# source = source_repo.get_by_id(1)
#
# job = Job(title='software_engineer', url='abc', pay='', schedule='', type='', description='', date_added=datetime.datetime.now())
# job.company = company
# job.source = source
#
# print(job_repo.add(job))
#
# job = job_repo.get_by_id(4)
# # for key, val in job.__dict__.items():
# #     print(key, val)
#
# # valid_attr = {k: v for (k, v) in job.__dict__.items() if k not in ['_sa_instance_state', 'id', 'date_added']}
# # for key, val in valid_attr.items():
# #     print(key, val)
# # print(valid_attr)
#
# job.pay = '$101'
# # job.id = 5
# job_repo.update(job)

# new_job = Job('software dev', 'abc', company_id=1 )