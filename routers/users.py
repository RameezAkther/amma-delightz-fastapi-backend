from fastapi import APIRouter, Depends
from schemas.user import UserResponse, UserUpdateProfile, UserUpdatePreferences
from fastapi import Body
from services.user_service import UserService
from core.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{userId}", response_model=UserResponse)
async def get_user(userId: str, current_user: User = Depends(get_current_user)):
    user = await UserService.get_user_by_id(userId)
    return user

@router.put("/{userId}/username", response_model=UserResponse)
async def update_username(userId: str, username: str = Body(embed=True), current_user: User = Depends(get_current_user)):
    return await UserService.update_username(userId, username)

@router.put("/{userId}/password", response_model=UserResponse)
async def update_password(userId: str, oldPassword: str = Body(...), newPassword: str = Body(...), current_user: User = Depends(get_current_user)):
    return await UserService.update_password(userId, oldPassword, newPassword)

@router.put("/{userId}/avatar", response_model=UserResponse)
async def update_avatar(userId: str, avatar: str = Body(embed=True), current_user: User = Depends(get_current_user)):
    return await UserService.update_avatar(userId, avatar)

@router.put("/{userId}/bio", response_model=UserResponse)
async def update_bio(userId: str, bio: str = Body(embed=True), current_user: User = Depends(get_current_user)):
    return await UserService.update_bio(userId, bio)

@router.put("/{userId}/location", response_model=UserResponse)
async def update_location(userId: str, location: str = Body(embed=True), current_user: User = Depends(get_current_user)):
    return await UserService.update_location(userId, location)

@router.put("/{userId}/preferences", response_model=UserResponse)
async def update_preferences(userId: str, prefs: UserUpdatePreferences, current_user: User = Depends(get_current_user)):
    return await UserService.update_preferences(userId, prefs)
