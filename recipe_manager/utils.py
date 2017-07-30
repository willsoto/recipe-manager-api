import pytz
import logging

from contextlib import contextmanager
from datetime import datetime

import sqlparse
import pygments
from pygments.lexers import SqlLexer, PythonLexer
from pygments.formatters import Terminal256Formatter


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


class SQLAlchemyFormatter(logging.Formatter):

    def format(self, record):
        message = record.getMessage()
        name = record.name

        if name == 'sqlalchemy.engine.base.Engine':
            if message.startswith('('):
                lexer = PythonLexer()
            else:
                lexer = SqlLexer()
            message = pygments.highlight(
                sqlparse.format(
                    message, reindent=True), lexer, Terminal256Formatter()).rstrip()

        return message
