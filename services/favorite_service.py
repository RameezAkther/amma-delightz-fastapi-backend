from fastapi import HTTPException
from models.favorite import Favorite
from models.recipe import Recipe
from typing import List

class FavoriteService:

    @staticmethod
    async def add_favorite(user_id: str, recipe_id: str) -> Favorite:
        existing = await Favorite.find_one(Favorite.userId == user_id, Favorite.recipeId == recipe_id)
        if existing:
            return existing # Already favorited
            
        fav = Favorite(userId=user_id, recipeId=recipe_id)
        await fav.insert()
        
        # Update recipe favoritesCount
        recipe = await Recipe.get(recipe_id)
        if recipe:
            recipe.favoritesCount += 1
            await recipe.save()
            
        return fav

    @staticmethod
    async def remove_favorite(user_id: str, recipe_id: str):
        fav = await Favorite.find_one(Favorite.userId == user_id, Favorite.recipeId == recipe_id)
        if fav:
            await fav.delete()
            
            recipe = await Recipe.get(recipe_id)
            if recipe and recipe.favoritesCount > 0:
                recipe.favoritesCount -= 1
                await recipe.save()

    @staticmethod
    async def get_user_favorites_only(user_id: str) -> List[dict]:
        # Return list of favorites (which have recipeId field that frontend expects)
        favorites = await Favorite.find(Favorite.userId == user_id).to_list()
        return favorites

    @staticmethod
    async def get_paginated_favorite_recipes(user_id: str, page: int, limit: int) -> dict:
        from services.recipe_service import RecipeService
        favorites = await Favorite.find(Favorite.userId == user_id).to_list()
        
        recipe_ids = [fav.recipeId for fav in favorites]
        
        # We need to fetch all these recipes
        recipes = []
        for rid in recipe_ids:
            r = await Recipe.get(rid)
            if r:
                recipes.append(r)
                
        total_elements = len(recipes)
        import math
        total_pages = math.ceil(total_elements / limit) if limit > 0 else 0
        
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paged_recipes = recipes[start_idx:end_idx] if start_idx < total_elements else []
        
        # Use _convert_to_meta so the frontend gets exactly what it expects (with string `id`)
        meta_recipes = [RecipeService._convert_to_meta(r) for r in paged_recipes]
        
        return {
            "recipes": meta_recipes,
            "pages": total_pages,
            "page": page
        }
