from pydantic import BaseModel, EmailStr, Field
from app.models.user import Role

#requests
class UserRegister(BaseModel):
    email: EmailStr
    name: str = Field(max_length=25, min_length=6)
    password: str = Field(min_length=8, max_length=20)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRoleUpdate(BaseModel):
    role: Role

class UserStatusUpdate(BaseModel):
    is_active: bool

#responses
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: Role
    is_active: bool
    model_config = {"from_attributes":True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str