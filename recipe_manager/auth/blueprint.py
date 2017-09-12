from flask import Blueprint, jsonify, redirect, request, session, url_for
from flask_login import login_required, login_user, logout_user

from ..extensions import db, login_manager, oauth
from ..users.models import User

blueprint = Blueprint('auth_blueprint', __name__)


google = oauth.remote_app(
    'google',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    app_key='GOOGLE',
)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)

    return user


@blueprint.route('/lr')
@login_required
def lr_test():
    me = google.get('userinfo')

    return jsonify({'data': me.data})


@blueprint.route('/google')
def do_login():
    return google.authorize(callback=url_for('.authorized', _external=True))


@blueprint.route('/logout')
def logout():
    session.pop('google_token', None)
    logout_user()

    return redirect('/')


@blueprint.route('/google/callback')
def authorized():
    resp = google.authorized_response()

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'],
        )

    google_token = resp['access_token']

    session['google_token'] = (google_token, '')

    google_user = google.get('userinfo')

    login_google_user(google_user.data['email'], google_token)

    return redirect('/')


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


def login_google_user(email, google_token):
    user = User.query.filter_by(email=email).first()

    if user is None:
        user = User(email=email, google_token=google_token)
        db.session.add(user)
        db.session.commit()

    login_user(user)
