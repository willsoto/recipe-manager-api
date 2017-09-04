from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Recipe, Tag, Ingredient, Instruction


class RecipeSchema(SQLAlchemyObjectType):

    class Meta:
        model = Recipe


class TagSchema(SQLAlchemyObjectType):

    class Meta:
        model = Tag


class IngredientSchema(SQLAlchemyObjectType):

    class Meta:
        model = Ingredient


class InstructionSchema(SQLAlchemyObjectType):

    class Meta:
        model = Instruction
