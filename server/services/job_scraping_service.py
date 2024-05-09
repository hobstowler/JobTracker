from server.models import User, Source, Search
from .base import BaseService
from server.services.scrapers import IndeedScrapingService


class JobScrapingService(BaseService):
    @staticmethod
    def scrape(user: User, source: Source, search: Search):
        if source.name == 'indeed':
            return IndeedScrapingService(user, source, search).scrape()
