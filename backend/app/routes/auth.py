from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.security import hash_password
from app.core.database import get_session
from app.models.user import User
from app.models.role import Role

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/test-hash")
def test_hash():
    sample_password = "sukha123"
    hashed = hash_password(sample_password)
    return {"original": sample_password, "hashed": hashed}


@router.get("/create-test-user")
def create_test_user(session: Session = Depends(get_session)):
    username = "manager1"
    password = "sukha123"

    # Check if user already exists
    statement = select(User).where(User.username == username)
    existing_user = session.exec(statement).first()

    if existing_user:
        return {"message": "User already exists", "username": username}

    user = User(
        username=username,
        hashed_password=hash_password(password),
        full_name="Manager Test",
        role=Role.manager
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "Manager user created successfully",
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    }
