from fastapi import HTTPException
from models.recipe import Recipe
from schemas.recipe import RecipeCreate, RecipeUpdate
from typing import List

class RecipeService:

    @staticmethod
    def _convert_to_meta(recipe: Recipe) -> dict:
        return {
            "id": str(recipe.id),
            "title": recipe.title,
            "description": recipe.description,
            "imageUrl": recipe.imageUrl if recipe.imageUrl is not None else [],
            "averageRating": recipe.averageRating,
            "views": recipe.views,
            "cuisine": recipe.cuisine,
            "category": recipe.category
        }

    @staticmethod
    async def get_paginated_recipes(
        page: int, limit: int, query: str = None, ingredient: str = None,
        cuisine: str = None, category: str = None, sort: str = None
    ) -> dict:
        # Fetch all recipes and filter in memory to match Java Spring Boot behavior exactly
        all_recipes = await Recipe.find_all().to_list()

        if query:
            q_lower = query.lower()
            all_recipes = [r for r in all_recipes if (r.title and q_lower in r.title.lower()) or (r.description and q_lower in r.description.lower())]

        if ingredient:
            ing_lower = ingredient.lower()
            all_recipes = [r for r in all_recipes if r.ingredients and any(ing.name and ing_lower in ing.name.lower() for ing in r.ingredients)]

        if cuisine:
            all_recipes = [r for r in all_recipes if r.cuisine and r.cuisine.lower() == cuisine.lower()]

        if category:
            all_recipes = [r for r in all_recipes if r.category and r.category.lower() == category.lower()]

        if sort:
            sort_lower = sort.lower()
            if sort_lower == "rating":
                all_recipes.sort(key=lambda x: x.averageRating if x.averageRating else 0, reverse=True)
            elif sort_lower == "views":
                all_recipes.sort(key=lambda x: x.views if x.views else 0, reverse=True)
            elif sort_lower == "newest":
                all_recipes.sort(key=lambda x: x.createdAt.timestamp() if x.createdAt else 0, reverse=True)

        total = len(all_recipes)
        import math
        total_pages = math.ceil(total / limit) if limit > 0 else 0
        start = (page - 1) * limit
        end = min(start + limit, total)
        
        paginated = all_recipes[start:end] if start < total else []
        meta_recipes = [RecipeService._convert_to_meta(r) for r in paginated]

        return {
            "recipes": meta_recipes,
            "total": total,
            "page": page,
            "pages": total_pages,
            "query": query,
            "ingredient": ingredient,
            "cuisine": cuisine,
            "category": category,
            "sort": sort
        }

    @staticmethod
    async def get_homepage_recipes() -> List[dict]:
        recipes = await Recipe.find_all().to_list()
        recipes.sort(key=lambda x: x.averageRating if x.averageRating else 0, reverse=True)
        return [RecipeService._convert_to_meta(r) for r in recipes[:3]]

    @staticmethod
    async def get_recipe_by_id(recipe_id: str) -> Recipe:
        recipe = await Recipe.get(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # update views
        recipe.views += 1
        await recipe.save()
        return recipe

    @staticmethod
    async def create_recipe(recipe_data: RecipeCreate) -> Recipe:
        recipe = Recipe(**recipe_data.model_dump())
        await recipe.insert()
        return recipe

    @staticmethod
    async def update_recipe(recipe_id: str, recipe_data: RecipeUpdate) -> Recipe:
        recipe = await RecipeService.get_recipe_by_id(recipe_id)
        update_data = recipe_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(recipe, key, value)
        await recipe.save()
        return recipe

    @staticmethod
    async def delete_recipe(recipe_id: str):
        recipe = await RecipeService.get_recipe_by_id(recipe_id)
        await recipe.delete()
