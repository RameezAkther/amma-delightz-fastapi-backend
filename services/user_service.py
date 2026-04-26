from fastapi import HTTPException
from datetime import datetime
from models.user import User
from schemas.user import UserUpdateProfile, UserUpdatePreferences
from core.security import get_password_hash

class UserService:
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> User:
        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def update_username(user_id: str, new_username: str) -> User:
        user = await UserService.get_user_by_id(user_id)
        # Check if username is taken
        existing_user = await User.find_one(User.username == new_username)
        if existing_user and str(existing_user.id) != user_id:
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = new_username
        user.updatedAt = datetime.utcnow()
        await user.save()
        return user

    @staticmethod
    async def update_password(user_id: str, old_password: str, new_password: str) -> User:
        from core.security import verify_password
        user = await UserService.get_user_by_id(user_id)
        if not verify_password(old_password, user.passwordHash):
            raise HTTPException(status_code=400, detail="Incorrect old password")
        user.passwordHash = get_password_hash(new_password)
        user.updatedAt = datetime.utcnow()
        await user.save()
        return user
        
    @staticmethod
    async def update_avatar(user_id: str, avatar_url: str) -> User:
        user = await UserService.get_user_by_id(user_id)
        user.profile.avatar = avatar_url
        user.updatedAt = datetime.utcnow()
        await user.save()
        return user

    @staticmethod
    async def update_bio(user_id: str, bio: str) -> User:
        user = await UserService.get_user_by_id(user_id)
        user.profile.bio = bio
        user.updatedAt = datetime.utcnow()
        await user.save()
        return user
        
    @staticmethod
    async def update_location(user_id: str, location: str) -> User:
        user = await UserService.get_user_by_id(user_id)
        user.profile.location = location
        user.updatedAt = datetime.utcnow()
        await user.save()
        return user

    @staticmethod
    async def update_preferences(user_id: str, prefs: UserUpdatePreferences) -> User:
        user = await UserService.get_user_by_id(user_id)
        user.preferences.diet = prefs.diet
        user.preferences.favoriteCuisines = prefs.favoriteCuisines
        user.updatedAt = datetime.utcnow()
        await user.save()
        return user
