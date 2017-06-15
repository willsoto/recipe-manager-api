from ..extensions import manager

from .models import Bookmark, Tag

bookmark_blueprint = manager.create_api_blueprint('bookmark', Bookmark)
tag_blueprint = manager.create_api_blueprint('tag', Tag)
