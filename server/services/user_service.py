from typing import Optional, List

from server.models import User, Job
from server.repositories import UserRepository
from server.services import BaseService


class UserService(BaseService):
    user_repo = UserRepository()

    def get_user_by_id(self, user_uuid: str) -> Optional[User]:
        return self.user_repo.get_by_id(user_uuid)

    def get_jobs_for_user(self, user_uuid: str) -> Optional[List[Job]]:
        return self.user_repo.get_jobs_for_user(user_uuid)
