import graphene
from flask import abort
from flask_login import current_user

from ..extensions import db
from .models import Recipe
from .schema import RecipeSchema


class RecipeInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreateRecipe(graphene.Mutation):

    class Arguments:
        recipe_data = RecipeInput(required=True)

    recipe = graphene.Field(RecipeSchema)

    @staticmethod
    def mutate(self, info, recipe_data=None):
        if not current_user.is_authenticated:
            abort(401)

        recipe = Recipe(**recipe_data)

        recipe.user = current_user

        db.session.add(recipe)
        db.session.commit()

        return CreateRecipe(recipe=recipe)
