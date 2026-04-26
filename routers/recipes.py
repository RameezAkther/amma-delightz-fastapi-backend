from fastapi import APIRouter, Depends, Query
from schemas.recipe import RecipeCreate, RecipeUpdate
from services.recipe_service import RecipeService
from core.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/api/recipes", tags=["recipes"])

@router.get("")
async def get_all_recipes(
    page: int = Query(1),
    limit: int = Query(9),
    q: str = Query(None),
    ingredient: str = Query(None),
    cuisine: str = Query(None),
    category: str = Query(None),
    sort: str = Query(None)
):
    return await RecipeService.get_paginated_recipes(
        page, limit, query=q, ingredient=ingredient,
        cuisine=cuisine, category=category, sort=sort
    )

@router.get("/homepage")
async def get_homepage_recipes():
    return await RecipeService.get_homepage_recipes()

@router.get("/{id}")
async def get_recipe(id: str):
    return await RecipeService.get_recipe_by_id(id)

@router.post("")
async def create_recipe(recipe_data: RecipeCreate, current_user: User = Depends(get_current_user)):
    return await RecipeService.create_recipe(recipe_data)

@router.put("/{id}")
async def update_recipe(id: str, recipe_data: RecipeUpdate, current_user: User = Depends(get_current_user)):
    return await RecipeService.update_recipe(id, recipe_data)

@router.delete("/{id}")
async def delete_recipe(id: str, current_user: User = Depends(get_current_user)):
    await RecipeService.delete_recipe(id)
    return {"message": "Recipe deleted successfully"}
