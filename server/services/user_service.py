from typing import Optional

from server.models import User
from server.repositories import UserRepository
from server.services import BaseService


class UserService(BaseService):
    user_repo = UserRepository()

    def get_user_by_id(self, user_uuid) -> Optional[User]:
        return self.user_repo.get_by_id(user_uuid)
