# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import sys
import logging

from flask import Flask
from flask_login import AnonymousUserMixin
from celery import Celery

import bookmarker.commands as commands
import bookmarker.extensions as extensions

from .settings import ProdConfig

from .auth.blueprint import blueprint as auth_blueprint

from .bookmarks import models as bookmark_models
from .bookmarks.api import bookmark_blueprint, tag_blueprint

from .users import models as user_models
from .users.api import blueprint as users_blueprint

log = logging.getLogger(__name__)


class AnonymousUser(AnonymousUserMixin):

    def __init__(self):
        self.user_id = None
        self.email = ''
        self.is_admin = False


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)

    app.config.from_object(config_object)

    setup_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_commands(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    extensions.bcrypt.init_app(app)
    extensions.db.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.oauth.init_app(app)
    extensions.manager.init_app(app)

    extensions.login_manager.anonymous_user = AnonymousUser

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')
    app.register_blueprint(bookmark_blueprint, url_prefix='/api/v1')
    app.register_blueprint(tag_blueprint, url_prefix='/api/v1')

    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': extensions.db,
            'User': user_models.User,
            'Bookmark': bookmark_models.Bookmark,
            'Tag': bookmark_models.Tag,
            'BookmarkTag': bookmark_models.BookmarkTag,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.drop)
    app.cli.add_command(commands.create)
    app.cli.add_command(commands.recreate)
    app.cli.add_command(commands.populate)
    app.cli.add_command(commands.routes)


def setup_logging(app):
    logging.basicConfig()

    log_level = app.config.get('LOG_LEVEL', logging.DEBUG)
    flask_oauthlib_log = logging.getLogger('flask_oauthlib')

    log.setLevel(log_level)

    logging.getLogger('sqlalchemy.engine').setLevel(log_level)

    flask_oauthlib_log.addHandler(logging.StreamHandler(sys.stdout))
    flask_oauthlib_log.setLevel(log_level)


def make_celery(app=None):
    app = app or create_app()

    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'])

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
