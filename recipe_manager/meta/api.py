from marshmallow_sqlalchemy import ModelSchemaOpts

from ..extensions import db, marshmallow


class BaseOpts(ModelSchemaOpts):

    def __init__(self, meta):
        if not hasattr(meta, 'sql_session'):
            meta.sqla_session = db.session
        super(BaseOpts, self).__init__(meta)


class BaseSchema(marshmallow.ModelSchema):
    OPTIONS_CLASS = BaseOpts
