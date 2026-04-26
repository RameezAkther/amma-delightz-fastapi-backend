from pydantic import BaseModel
from typing import Optional, List, Any
from models.recipe import Ingredient, CreatedBy

class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cuisine: Optional[str] = None
    category: Optional[str] = None
    ingredients: List[Ingredient] = []
    steps: List[str] = []
    prepTime: int = 0
    cookTime: int = 0
    totalTime: int = 0
    servings: int = 0
    tags: List[str] = []
    createdBy: Optional[CreatedBy] = None
    imageUrl: List[str] = []

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cuisine: Optional[str] = None
    category: Optional[str] = None
    ingredients: Optional[List[Ingredient]] = None
    steps: Optional[List[str]] = None
    prepTime: Optional[int] = None
    cookTime: Optional[int] = None
    totalTime: Optional[int] = None
    servings: Optional[int] = None
    tags: Optional[List[str]] = None
    imageUrl: Optional[List[str]] = None
