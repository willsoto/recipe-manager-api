from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import User


class UserSchema(SQLAlchemyObjectType):

    class Meta:
        model = User
