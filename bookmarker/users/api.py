import simplejson as json
from flask_login import current_user

from ..extensions import manager

from .models import User

blueprint = manager.create_api_blueprint('user', User, methods=['GET'])


@blueprint.route('/users/me')
def me():
    return json.dumps({
        'user_id': current_user.user_id,
        'email': current_user.email,
        'is_admin': current_user.is_admin,
    })
