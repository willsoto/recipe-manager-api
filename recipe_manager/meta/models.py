import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql.expression import text

from ..extensions import db
from ..utils import utcnow


class TimestampMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), default=utcnow)
    updated_at = db.Column(
        db.DateTime(
            timezone=True,
        ),
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
        default=utcnow,
        onupdate=utcnow,
    )


class BaseModel(TimestampMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    def __repr__(self):
        return self.__str__()


def primary_key(**kwargs):
    return db.Column(pg.UUID, primary_key=True, server_default=text('gen_random_uuid()'), **kwargs)
