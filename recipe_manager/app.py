# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import sys
import logging
import logging.config

from flask import Flask
from flask_login import AnonymousUserMixin
from celery import Celery

import recipe_manager.commands as commands
import recipe_manager.extensions as extensions

from .settings import ProdConfig

from .auth.blueprint import blueprint as auth_blueprint

from .recipes import models as recipe_models
from .recipes.api import blueprint as recipes_blueprint

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
    extensions.marshmallow.init_app(app)

    extensions.login_manager.anonymous_user = AnonymousUser

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(users_blueprint, url_prefix='/api')
    app.register_blueprint(recipes_blueprint, url_prefix='/api')

    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': extensions.db,
            'User': user_models.User,
            'Recipe': recipe_models.Recipe,
            'Tag': recipe_models.Tag,
            'RecipeTag': recipe_models.RecipeTag,
            'Ingredient': recipe_models.Ingredient,
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
    log_level = app.config.get('LOG_LEVEL', logging.DEBUG)

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            'sqlalchemy.engine': {
                'level': logging.INFO,
                'handlers': ['sql']
            },
            'flask_oauthlib': {
                'level': log_level,
                'handlers': ['default']
            }
        },
        'handlers': {
            'default': {
                'level': log_level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'sql': {
                'level': logging.INFO,
                'formatter': 'sql',
                'class': 'logging.StreamHandler',
            }
        },
        'formatters': {
            'standard': {
                'format': '%(levelname)s %(message)s',
            },
            'sql': {
                'format': '[%(levelname)s] %(message)s',
                'class': 'recipe_manager.utils.SQLAlchemyFormatter'
            },
        }
    })


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
