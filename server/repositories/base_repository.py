from abc import ABC, abstractmethod
from functools import wraps

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from server.models.base import Base

DEFAULT_LIMIT = 100


def with_session(func):
    @wraps(func)
    def _with_session(self, *args, **kwargs):
        with self.session_maker.begin() as session:
            # kwargs['session'] = session
            return func(self, session, *args, **kwargs)

    return _with_session


class BaseRepository(ABC):
    engine: Engine
    session_maker: sessionmaker

    def __init__(self) -> None:
        self.engine = create_engine('mysql+pymysql://root:root@localhost/job', echo=False, pool_pre_ping=True, pool_recycle=3600)
        self.session_maker = sessionmaker(bind=self.engine, expire_on_commit=False)

    def create_db(self) -> None:
        Base.metadata.create_all(self.engine)

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def get_by_id(self, obj_id: int):
        pass

    @abstractmethod
    def update(self, obj):
        pass

    @abstractmethod
    def delete(self, obj_id: int):
        pass


# b = BaseRepository()
# b.create_db()