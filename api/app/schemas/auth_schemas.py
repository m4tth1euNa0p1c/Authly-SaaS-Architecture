from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    firebase_token: Optional[str] = None

    @validator('email', pre=True, always=True)
    def normalize_email(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @validator('email', pre=True, always=True)
    def normalize_email(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @validator('first_name', 'last_name', pre=True, always=True)
    def trim_names(cls, v):
        if v is None:
            return ""
        return v.strip()

    @validator('password')
    def check_password_complexity(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit.')
        if not re.search(r'[@$!%*?&]', v):
            raise ValueError('Password must contain at least one special character (@$!%*?&).')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        return v

class RegisterResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
