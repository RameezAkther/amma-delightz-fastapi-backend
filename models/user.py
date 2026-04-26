from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Profile(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

class Preferences(BaseModel):
    diet: List[str] = Field(default_factory=list)
    favoriteCuisines: List[str] = Field(default_factory=list)

class User(Document):
    username: str
    email: str
    passwordHash: str
    role: str = "user"
    
    profile: Profile = Field(default_factory=Profile)
    preferences: Preferences = Field(default_factory=Preferences)
    
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
