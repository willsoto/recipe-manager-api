from ..extensions import db
from ..meta import BaseModel


class Bookmark(BaseModel):

    __tablename__ = 'bookmarks'

    bookmark_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', back_populates='bookmarks')

    tags = db.relationship('Tag', secondary='bookmark_tags', back_populates='bookmarks')

    def __str__(self):
        return '<Bookmark {} {}>'.format(self.bookmark_id, self.url)

    def id(self):
        return self.bookmark_id


class Tag(BaseModel):

    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    bookmarks = db.relationship('Bookmark', secondary='bookmark_tags', back_populates='tags')

    def __str__(self):
        return '<Tag {} {}>'.format(self.tag_id, self.name)

    def id(self):
        return self.tag_id


class BookmarkTag(BaseModel):

    __tablename__ = 'bookmark_tags'

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
    bookmark_id = db.Column(db.Integer, db.ForeignKey('bookmarks.bookmark_id'), primary_key=True)

    def __str__(self):
        return '<BookmarkTag <Bookmark {}> <Tag {}>>'.format(self.bookmark_id, self.tag_id)
