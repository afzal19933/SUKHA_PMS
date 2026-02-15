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
