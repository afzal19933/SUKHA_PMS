from fastapi import APIRouter
from app.core.security import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/test-hash")
def test_hash():
    sample_password = "sukha123"
    hashed = hash_password(sample_password)
    return {
        "original": sample_password,
        "hashed": hashed
    }
from app.models.user import User
from app.models.role import Role

@router.get("/create-test-user")
def create_test_user():
    # Simulated user creation (no database yet)
    username = "manager1"
    password = "sukha123"
    role = Role.manager

    hashed = hash_password(password)

    user = {
        "username": username,
        "hashed_password": hashed,
        "role": role
    }

    return {
        "message": "Test user created (simulation)",
        "user": user
    }
