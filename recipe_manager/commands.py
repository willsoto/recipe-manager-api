# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from operator import attrgetter
from subprocess import call

import click
from flask.cli import with_appcontext
from flask_script import prompt_bool

from .extensions import db

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)


@click.command()
@click.option(
    '-f', '--fix-imports', default=False, is_flag=True,
    help='Fix imports using isort, before linting',
)
def lint(fix_imports):
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    root_files = glob('*.py')
    root_directories = [
        name for name in next(os.walk('.'))[1] if not name.startswith('.')
    ]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip
    ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


@click.command()
@with_appcontext
def drop():
    """Drops database tables"""
    if prompt_bool('Are you sure you want to lose all your data'):
        db.reflect()
        db.drop_all()


@click.command()
@with_appcontext
def create(default_data=False, sample_data=False):
    """Creates database tables from sqlalchemy models"""
    db.create_all()
    if default_data or sample_data:
        populate(default_data, sample_data)


@click.command()
@with_appcontext
def recreate(default_data=False, sample_data=False):
    """Recreates database tables (same as issuing 'drop' and then 'create')"""
    drop()

    create(default_data, sample_data)


@click.command()
@with_appcontext
def populate(default_data=True, sample_data=False):
    """Populate database with default data"""
    from fixtures import dbfixture

    if default_data:
        from fixtures import UserData
        default_data = dbfixture.data(UserData)
        default_data.setup()


@click.command('routes', short_help='Show application routes.')
@with_appcontext
def routes():
    """Prints all the given routes for an application"""
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app
    routes = []
    ignored_methods = set(['HEAD', 'OPTIONS'])
    sorted_rules = sorted(app.url_map.iter_rules(), key=attrgetter('endpoint'))

    for rule in sorted_rules:
        sorted_methods = sorted(rule.methods - ignored_methods)
        methods = ', '.join(sorted_methods)
        routes.append([rule.endpoint, methods, rule.rule])

    cols = zip(*routes)
    col_widths = [max(len(value) for value in col) for col in cols]
    line = ' '.join(['%%-%ds' % width for width in col_widths])

    previous_endpoint = None
    for route in routes:
        current_endpoint = route[0]
        if previous_endpoint == current_endpoint:
            current_endpoint = ''

        previous_endpoint = route[0]

        print(line % tuple([current_endpoint] + route[1:]))
