from flask import Blueprint, request, current_app, jsonify
from flask_login import current_user, login_required
from marshmallow import fields

from ..extensions import db
from ..meta import BaseSchema

from .models import Recipe, Tag

blueprint = Blueprint('recipes', __name__)


class TagSchema(BaseSchema):

    class Meta:
        model = Tag
        exclude = ('recipes', 'created_at', 'updated_at',)

tag_schema = TagSchema()


class RecipeSchema(BaseSchema):

    tags = fields.Nested(TagSchema, many=True, exclude=('recipes',))

    class Meta:
        model = Recipe
        exclude = ('user',)


recipe_schema = RecipeSchema()


@blueprint.route('/recipes', methods=('GET',))
def get_all_recipes():
    recipes = Recipe.query.all()

    current_app.logger.debug(recipes)

    result = recipe_schema.dump(recipes, many=True)

    return jsonify(result.data)


@blueprint.route('/recipes/<int:recipe_id>')
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if recipe is None:
        return jsonify({
            'message': 'Recipe not found'
        }), 404

    current_app.logger.debug(recipe)

    result = recipe_schema.dump(recipe)

    return jsonify(result.data)


@blueprint.route('/recipes', methods=('POST',))
@login_required
def create_recipe():
    json_data = request.get_json()
    recipe, errors = recipe_schema.load(json_data)

    if errors:
        return jsonify(errors), 422

    current_app.logger.debug(recipe)
    current_app.logger.debug(current_user)

    recipe.user = current_user

    db.session.add(recipe)
    db.session.commit()

    return recipe_schema.jsonify(recipe)


@blueprint.route('/tags', methods=('GET',))
def get_all_tags():
    tags = Tag.query.all()

    current_app.logger.debug(tags)

    result = tag_schema.dump(tags, many=True)

    return jsonify(result.data)
