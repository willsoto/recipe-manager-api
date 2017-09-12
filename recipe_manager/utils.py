import logging
from contextlib import contextmanager
from datetime import datetime

import pygments
import pytz
import sqlparse
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer, SqlLexer


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
                message = sqlparse.format(message, reindent=True, keyword_case='upper')

            message = pygments.highlight(message, lexer, Terminal256Formatter()).rstrip()

        return message
