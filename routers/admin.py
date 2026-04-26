from fastapi import APIRouter, Depends, HTTPException
from core.dependencies import get_current_admin_user
from models.user import User
from typing import List

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/users", response_model=dict)
async def get_all_users(current_user: User = Depends(get_current_admin_user)):
    users = await User.find_all().to_list()
    # Return in format expected by frontend
    return {
        "users": [{"id": str(u.id), "username": u.username, "email": u.email, "role": u.role.upper(), "profile": u.profile.model_dump()} for u in users],
        "pages": 1 # For now, return 1 as pagination is not fully implemented
    }

@router.delete("/users/{id}", response_model=dict)
async def delete_user(id: str, current_user: User = Depends(get_current_admin_user)):
    user = await User.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"message": "User deleted successfully"}
