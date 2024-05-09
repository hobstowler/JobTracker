from typing import List, Optional, Type

from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from server.models import Company
from server.repositories.base_repository import BaseRepository, with_session, DEFAULT_LIMIT


class CompanyRepository(BaseRepository):
    @with_session
    def add(self, session: Session, company: Company) -> str:
        session.add(company)
        session.flush()

        return company.uuid

    @with_session
    def add_multiple(self, session: Session, companies: List[Company]) -> None:
        session.bulk_save_objects(companies)
        # TODO

    @with_session
    def get(self, session: Session, limit=DEFAULT_LIMIT, offset: int = 0) -> list[Type[Company]]:
        companies = session.query(Company).limit(limit).offset(offset).all()

        return companies

    @with_session
    def get_by_id(self, session: Session, company_uuid: str) -> Optional[Company]:
        company = session.query(Company).where(Company.uuid == company_uuid).first()

        return company

    @with_session
    def get_by_name(self, session: Session, company_name: str) -> Optional[Company]:
        company = session.query(Company).where(Company.name == company_name).first()

        return company

    @with_session
    def update(self, session: Session, company: Company) -> None:
        valid_attr = {k: v for (k, v) in company.__dict__.items() if k not in ['_sa_instance_state', 'uuid']}

        session.query(Company).where(Company.uuid == company.uuid).update(valid_attr)

    @with_session
    def delete(self, session: Session, company_uuid: str) -> None:
        company_to_delete = session.query(Company).where(Company.uuid == company_uuid).first()

        if company_to_delete:
            session.delete(company_to_delete)
