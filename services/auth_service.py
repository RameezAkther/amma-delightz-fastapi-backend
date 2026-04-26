from fastapi import HTTPException, status
from models.user import User, Profile, Preferences
from schemas.user import UserCreate
from schemas.auth import LoginRequest, TokenResponse
from core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from config import settings

class AuthService:
    
    @staticmethod
    async def signup(user_data: UserCreate) -> User:
        existing_user = await User.find_one({"$or": [{"username": user_data.username}, {"email": user_data.email}]})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
            
        hashed_password = get_password_hash(user_data.passwordHash)
        
        prof = Profile()
        if user_data.profile:
            prof = Profile(
                name=user_data.profile.name,
                avatar=user_data.profile.avatar,
                bio=user_data.profile.bio,
                location=user_data.profile.location
            )

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            passwordHash=hashed_password,
            profile=prof,
            preferences=Preferences()
        )
        await new_user.insert()
        return new_user

    @staticmethod
    async def login(login_data: LoginRequest) -> TokenResponse:
        user = await User.find_one(User.email == login_data.email)
        if not user or not verify_password(login_data.password, user.passwordHash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        access_token_expires = timedelta(minutes=settings.jwt_expiration_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return TokenResponse(token=access_token, userId=str(user.id))
