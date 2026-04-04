from enum import Enum
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Role(str, Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

#user table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=25)
    hashed_password: str = Field(max_length=100)
    role: Role = Field(default=Role.viewer)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
