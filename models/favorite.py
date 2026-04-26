from beanie import Document
from pydantic import Field
from datetime import datetime

class Favorite(Document):
    userId: str
    recipeId: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "favorites"
