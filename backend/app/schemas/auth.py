# app/schemas/auth.py  (recommended location)

from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum


# -------------------------------------------------------------------
# ROLE ENUM (recommended for permission control)
# -------------------------------------------------------------------
class Role(str, Enum):
    manager = "manager"
    staff = "staff"
    admin = "admin"


# -------------------------------------------------------------------
# LOGIN REQUEST
# -------------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


# -------------------------------------------------------------------
# TOKEN RESPONSE (JWT)
# -------------------------------------------------------------------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# -------------------------------------------------------------------
# USER RESPONSE (SAFE PUBLIC DATA)
# -------------------------------------------------------------------
class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: Role

    # ✅ Pydantic v2 modern config
    model_config = ConfigDict(from_attributes=True)
