# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
manager = APIManager(flask_sqlalchemy_db=db)
oauth = OAuth()
