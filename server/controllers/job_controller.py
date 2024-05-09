from .base_controller import BaseController
from ..services import JobService, UserService, SourceService, SearchService


class JobController(BaseController):
    job_service = JobService
    user_service = UserService
    source_service = SourceService
    search_service = SearchService

    def scrape(self, user_uuid: str, source_name: str, search_uuid: str):
        user = self.user_service().get_user_by_id(user_uuid)
        source = self.source_service().get_source_by_name(source_name)
        search = self.search_service().get_search_by_id(search_uuid)

        self.job_service().scrape(user=user, source=source, search=search)

    def apply(self, user_uuid: str, job_uuids: list):
        pass

    def get_jobs(self, user_uuid: str, job_ids: list = None):
        if job_ids is None:
            return self.user_service().get_jobs_for_user(user_uuid)
