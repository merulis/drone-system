from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session

from app.core import settings


class SyncAsyncDataBase:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_engine(url=url, echo=echo)
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = scoped_session(
            session_factory=self.session_factory,
        )
        return session

    def session_dependency(self):
        """return new sqlalchemy.Session"""
        with self.session_factory() as session:
            yield session

    def scoped_session_dependency(self):
        """
        return scoped sqlalchemy.Session
        """
        session = self.get_scoped_session()
        yield session
        session.close()


sync_db = SyncAsyncDataBase(
    str(settings.DB.SQLALCHEMY_DATABASE_URL),
    settings.DB.ECHO,
)
