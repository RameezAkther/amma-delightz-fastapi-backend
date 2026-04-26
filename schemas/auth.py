from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    token: str
    userId: str

class IsAdminResponse(BaseModel):
    isAdmin: bool
