from typing import Literal
from pydantic import BaseModel, EmailStr, Field

Role = Literal["Admin", "Viewer"]

class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Role = "Viewer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role
