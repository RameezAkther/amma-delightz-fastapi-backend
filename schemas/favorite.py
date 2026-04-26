from pydantic import BaseModel
from typing import List

class FavoriteRequest(BaseModel):
    userId: str
    recipeId: str
