from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreateProfile(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    passwordHash: str
    profile: Optional[UserCreateProfile] = None

class UserUpdateProfile(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class UserUpdatePreferences(BaseModel):
    diet: List[str]
    favoriteCuisines: List[str]

from models.user import Profile, Preferences
from beanie import PydanticObjectId

class UserResponse(BaseModel):
    id: PydanticObjectId
    username: str
    email: str
    role: str
    profile: Profile
    preferences: Preferences

    class Config:
        from_attributes = True
