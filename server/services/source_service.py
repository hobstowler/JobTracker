from typing import Optional

from server.models import Source
from server.repositories import SourceRepository
from server.services import BaseService


class SourceService(BaseService):
    source_repo = SourceRepository()

    def get_source_by_id(self, source_uuid) -> Optional[Source]:
        return self.source_repo.get_by_id(source_uuid)

    def get_source_by_name(self, source_name) -> Optional[Source]:
        return self.source_repo.get_by_name(source_name)
