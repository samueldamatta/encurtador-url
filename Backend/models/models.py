from pydantic import BaseModel
from datetime import datetime

class UrlCreate(BaseModel):
    long_url: str

class UrlInDB(BaseModel):
    id: str
    long_url: str
    created_at: datetime
    user_id: str

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserInDB(BaseModel):
    id: str
    email: str
    password: str

class User(BaseModel):
    """User model without password for responses"""
    id: str
    email: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str