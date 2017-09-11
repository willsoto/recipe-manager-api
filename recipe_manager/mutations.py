import graphene

from .recipes.mutations import CreateRecipe


class Mutation(graphene.ObjectType):
    create_recipe = CreateRecipe.Field()
