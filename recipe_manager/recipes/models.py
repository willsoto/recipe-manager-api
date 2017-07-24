from ..extensions import db
from ..meta import BaseModel


class Recipe(BaseModel):

    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', back_populates='recipes')

    tags = db.relationship('Tag', secondary='recipe_tags', back_populates='recipes', lazy='joined')

    def __str__(self):
        return '<Recipe {} {}>'.format(self.recipe_id, self.name)


class Tag(BaseModel):

    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    recipes = db.relationship('Recipe', secondary='recipe_tags', back_populates='tags')

    def __str__(self):
        return '<Tag {} {}>'.format(self.tag_id, self.name)


class RecipeTag(BaseModel):

    __tablename__ = 'recipe_tags'

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), primary_key=True)

    def __str__(self):
        return '<RecipeTag <Recipe {}> <Tag {}>>'.format(self.recipe_id, self.tag_id)
