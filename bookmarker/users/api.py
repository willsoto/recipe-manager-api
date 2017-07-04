from flask import Blueprint
from flask_login import current_user

from ..meta import BaseSchema

from .models import User

blueprint = Blueprint('users', __name__)


class UserSchema(BaseSchema):

    class Meta:
        model = User


user_schema = UserSchema()


@blueprint.route('/users/me', methods=('GET',))
def me():
    return user_schema.jsonify(current_user)
