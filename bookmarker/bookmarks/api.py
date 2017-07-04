from flask import Blueprint, request, current_app, jsonify
from flask_login import current_user
from marshmallow import fields

from ..extensions import db
from ..meta import BaseSchema

from .models import Bookmark, Tag

blueprint = Blueprint('bookmarks', __name__)


class TagSchema(BaseSchema):

    class Meta:
        model = Tag

tag_schema = TagSchema()


class BookmarkSchema(BaseSchema):

    tags = fields.Nested(TagSchema, many=True, exclude=('bookmarks',))

    class Meta:
        model = Bookmark


bookmark_schema = BookmarkSchema()


@blueprint.route('/bookmarks', methods=('GET',))
def get_all_bookmarks():
    bookmarks = Bookmark.query.all()

    current_app.logger.debug(bookmarks)

    result = bookmark_schema.dump(bookmarks, many=True)

    return jsonify(result.data)


@blueprint.route('/bookmarks', methods=('POST',))
def create_bookmark():
    json_data = request.get_json()
    bookmark, errors = bookmark_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    current_app.logger.debug(bookmark)

    bookmark.user = current_user

    db.session.add(bookmark)
    db.session.commit()

    return bookmark_schema.jsonify(bookmark)
