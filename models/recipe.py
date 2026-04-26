from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class Ingredient(BaseModel):
    name: str
    quantity: Optional[Any] = None
    unit: Optional[str] = None
    notes: Optional[str] = None

class CreatedBy(BaseModel):
    name: str

class Recipe(Document):
    title: str
    description: Optional[str] = None
    cuisine: Optional[str] = None
    category: Optional[str] = None
    
    ingredients: List[Ingredient] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    
    prepTime: int = 0
    cookTime: int = 0
    totalTime: int = 0
    servings: int = 0
    tags: List[str] = Field(default_factory=list)
    
    createdBy: Optional[CreatedBy] = None
    
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    
    ratingsCount: int = 0
    averageRating: float = 0.0
    favoritesCount: int = 0
    views: int = 0
    imageUrl: List[str] = Field(default_factory=list)

    class Settings:
        name = "recipe"
