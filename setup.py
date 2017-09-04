#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.1.0'

setup(
    name='recipe_manager',
    version=__version__,
    author='Will Soto',
    author_email='will.soto9+github@gmail.com',
    url='https://github.com/willsoto/recipe-manager-api',
    license='Apache-2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'alembic',
        'celery',
        'click',
        'configargparse',
        'dateutils',
        'fixture',
        'flask',
        'Flask-Bcrypt',
        'Flask-GraphQL',
        'Flask-Login',
        'flask-marshmallow',
        'Flask-OAuthlib',
        'Flask-Script',
        'flask-shell-ipython',
        'Flask-SQLAlchemy',
        'graphene',
        'graphene-sqlalchemy',
        'ipdb',
        'ipython',
        'marshmallow-sqlalchemy',
        'oauthlib',
        'psycopg2',
        'Pygments',
        'python-dateutil',
        'pytz',
        'redis',
        'simplejson',
        'SQLAlchemy',
        'sqlparse',
        'uwsgi',
        'Werkzeug',
    ],
)
