from server.repositories import SearchRepository
from server.services import BaseService


class SearchService(BaseService):
    search_repo = SearchRepository()

    def get_search_by_id(self, search_uuid):
        return self.search_repo.get_by_id(search_uuid)
