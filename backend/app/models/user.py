from sqlmodel import SQLModel, Field
from app.models.role import Role

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    full_name: str
    role: Role
