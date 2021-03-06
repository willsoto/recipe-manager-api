from flask_login import UserMixin

from ..extensions import db
from ..meta import BaseModel, primary_key


class User(BaseModel, UserMixin):

    __tablename__ = 'users'

    user_id = primary_key()
    email = db.Column(db.Text, nullable=False)
    google_token = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    recipes = db.relationship('Recipe', back_populates='user')

    def __str__(self):
        return '<User {} {}>'.format(self.user_id, self.email)

    def get_id(self):
        return self.user_id
