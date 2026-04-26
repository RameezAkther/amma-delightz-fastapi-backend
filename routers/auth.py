from fastapi import APIRouter, Depends
from schemas.user import UserCreate
from schemas.auth import LoginRequest, TokenResponse, IsAdminResponse
from services.auth_service import AuthService
from core.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup", response_model=dict)
async def signup(user_data: UserCreate):
    user = await AuthService.signup(user_data)
    return {"message": "User registered successfully", "userId": str(user.id)}

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    return await AuthService.login(login_data)

@router.get("/is-admin", response_model=IsAdminResponse)
async def is_admin(current_user: User = Depends(get_current_user)):
    return IsAdminResponse(isAdmin=current_user.role == "admin")
