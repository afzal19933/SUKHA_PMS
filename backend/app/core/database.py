from sqlmodel import SQLModel, create_engine, Session

# Local SQLite database (simple and beginner safe)
DATABASE_URL = "sqlite:///./sukha.db"

engine = create_engine(
    DATABASE_URL,
    echo=True  # shows SQL logs (good for learning)
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
