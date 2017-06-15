import pytz
from contextlib import contextmanager
from datetime import datetime


def utcnow():
    utc_now = datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=pytz.utc)
    return utc_now


def create_session_scope_manager(Session):
    @contextmanager
    def session_scope():
        """Provide a transactional scope around a series of operations."""
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
