from fastapi import APIRouter, Depends, Query
from schemas.favorite import FavoriteRequest
from services.favorite_service import FavoriteService
from core.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/api/favorites", tags=["favorites"])

@router.post("")
async def add_favorite(request: FavoriteRequest, current_user: User = Depends(get_current_user)):
    fav = await FavoriteService.add_favorite(request.userId, request.recipeId)
    return {"message": "Favorite added", "id": str(fav.id)}

@router.delete("")
async def remove_favorite(request: FavoriteRequest, current_user: User = Depends(get_current_user)):
    await FavoriteService.remove_favorite(request.userId, request.recipeId)
    return {"message": "Favorite removed"}

@router.get("/{userId}")
async def get_favorites(userId: str, current_user: User = Depends(get_current_user)):
    return await FavoriteService.get_user_favorites_only(userId)

@router.get("/{userId}/paged")
async def get_favorites_paged(
    userId: str, 
    page: int = Query(1), 
    limit: int = Query(9), 
    current_user: User = Depends(get_current_user)
):
    return await FavoriteService.get_paginated_favorite_recipes(userId, page, limit)
