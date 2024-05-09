from typing import List, Optional, Type

from sqlalchemy import Uuid
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session

from server.models import User, Job
from server.repositories import JobRepository
from server.repositories.base_repository import BaseRepository, with_session, DEFAULT_LIMIT


class UserRepository(BaseRepository):
    @with_session
    def add(self, session: Session, user: User) -> User:
        session.add(user)
        session.flush()

        return user

    @with_session
    def add_job_to_user(self, session: Session, user: User, job: Job) -> None:
        try:
            user = session.query(User).where(User.uuid == user.uuid).first()
            user.jobs.append(job)
        except InvalidRequestError:
            pass

    @with_session
    def get(self, session: Session, limit=DEFAULT_LIMIT, offset: int = 0) -> list[Type[User]]:
        users = session.query(User).limit(limit).offset(offset).all()

        return users

    @with_session
    def get_by_id(self, session: Session, user_uuid: str) -> Optional[User]:
        user = session.query(User).where(User.uuid == user_uuid).first()

        return user

    @with_session
    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        user = session.query(User).where(User.email == email).first()

        return user

    @with_session
    def update(self, session: Session, user: User) -> None:
        valid_attr = {k: v for (k, v) in user.__dict__.items() if k not in ['_sa_instance_state', 'id']}

        session.query(User).where(User.uuid == user.uuid).update(valid_attr)

    @with_session
    def delete(self, session: Session, user_uuid: str) -> None:
        user_to_delete = session.query(User).where(User.uuid == user_uuid).first()

        if user_to_delete:
            session.delete(user_to_delete)


# user_repo = UserRepository()
# user = user_repo.get_by_email('jameshtowler@gmail.com')
#
# job_repo = JobRepository()
# job = job_repo.get_by_id('4653f8be-a94d-4804-8636-e695d69aa29e')
#
# user_repo.add_job_to_user(user.uuid, job)
# user = User('abcdefg@a.com')
# user_repo.add(user)
# print(user.uuid)
#
# user = User('jameshtowler@gmail.com')
# user.first_name = 'James'
# user.last_name = 'Towler'
# user.preferred_first_name = 'Hobs'
#
# user_repo.update(user)
# user_repo.add(user)
