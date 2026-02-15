from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.core.dependencies import get_current_user
from app.core.permissions import require_roles


router = APIRouter(prefix="/auth", tags=["Authentication"])


# ======================================================
# SIMPLE WELCOME MESSAGE (NAME ONLY)
# ======================================================

def build_welcome_message(user: User) -> str:
    return f"Welcome {user.full_name} 👋"


# ======================================================
# LOGIN (OAuth2 Swagger Compatible)
# ======================================================

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    # Find user
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Create JWT token
    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token="",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ======================================================
# CURRENT USER PROFILE + WELCOME MESSAGE
# ======================================================

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    welcome_message = build_welcome_message(current_user)

    return {
        "message": welcome_message,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "full_name": current_user.full_name,
            "role": current_user.role,
        },
    }


# ======================================================
# MANAGER / ADMIN TEST ENDPOINT
# ======================================================

@router.get("/manager-only")
def manager_only_test(user: User = Depends(require_roles(["admin", "manager"]))):
    return {"message": f"Hello {user.full_name}"}
