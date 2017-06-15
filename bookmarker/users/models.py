from flask_login import UserMixin

from ..extensions import db
from ..meta import BaseModel


class User(BaseModel, UserMixin):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    google_token = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    bookmarks = db.relationship('Bookmark', back_populates='user')

    def __str__(self):
        return '<User {} {}>'.format(self.user_id, self.email)

    def get_id(self):
        return self.user_id

    @property
    def id(self):
        return self.user_id
