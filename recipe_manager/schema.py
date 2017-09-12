import graphene
from flask_login import current_user
from graphene import relay
from recipe_manager.mutations import Mutation

from .recipes.schema import IngredientSchema, InstructionSchema, RecipeSchema, TagSchema
from .users.schema import UserSchema


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    recipes = graphene.List(RecipeSchema)
    tags = graphene.List(TagSchema)
    ingredients = graphene.List(IngredientSchema)
    instructions = graphene.List(InstructionSchema)
    current_user = graphene.Field(UserSchema)

    def resolve_recipes(self, info):
        query = RecipeSchema.get_query(info)

        return query.all()

    def resolve_current_user(self, info):
        query = UserSchema.get_query(info).filter_by(user_id=current_user.user_id)

        return query.first()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    auto_camelcase=False,
    types=[
        UserSchema,
        RecipeSchema,
        TagSchema,
        IngredientSchema,
        InstructionSchema,
    ],
)
