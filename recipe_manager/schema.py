import graphene
from graphene import relay
from flask_login import current_user

from .recipes.schema import RecipeSchema, TagSchema, IngredientSchema, InstructionSchema
from .users.schema import UserSchema


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    recipes = graphene.List(RecipeSchema)
    tags = graphene.List(TagSchema)
    ingredients = graphene.List(IngredientSchema)
    instructions = graphene.List(InstructionSchema)
    current_user = graphene.Field(UserSchema)

    def resolve_recipes(self, args, context, info):
        query = RecipeSchema.get_query(info)

        return query.all()

    def resolve_current_user(self, args, context, info):
        query = UserSchema.get_query({
            'user_id': current_user.user_id
        })

        return query.first()

schema = graphene.Schema(
    query=Query,
    auto_camelcase=False,
    types=[
        UserSchema,
        RecipeSchema,
        TagSchema,
        IngredientSchema,
        InstructionSchema])
