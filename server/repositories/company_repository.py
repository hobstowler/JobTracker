from typing import List, Optional, Type

from sqlalchemy.orm import Session

from server.models import Company
from server.repositories.base_repository import BaseRepository, with_session, DEFAULT_LIMIT


class CompanyRepository(BaseRepository):
    @with_session
    def add(self, session: Session, company: Company) -> int:
        session.add(company)
        session.flush()

        return company.id

    @with_session
    def add_multiple(self, session: Session, companies: List[Company]) -> None:
        session.bulk_save_objects(companies)

    @with_session
    def get(self, session: Session, limit=DEFAULT_LIMIT, offset: int = 0) -> list[Type[Company]]:
        companies = session.query(Company).limit(limit).offset(offset).all()

        return companies

    @with_session
    def get_by_id(self, session: Session, company_id: int) -> Optional[Company]:
        company = session.query(Company).where(Company.id == company_id).first()

        return company

    @with_session
    def get_by_name(self, session: Session, company_name: str) -> Optional[Company]:
        source = session.query(Company).where(Company.name == company_name).first()

        return source

    @with_session
    def update(self, session: Session, company: Company) -> None:
        valid_attr = {k: v for (k, v) in company.__dict__.items() if k not in ['_sa_instance_state', 'id']}

        session.query(Company).where(Company.id == company.id).update(valid_attr)

    @with_session
    def delete(self, session: Session, company_id: int) -> None:
        company_to_delete = session.query(Company).where(Company.id == company_id).first()

        if company_to_delete:
            session.delete(company_to_delete)
