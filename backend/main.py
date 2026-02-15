from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.core.database import create_db_and_tables

app = FastAPI(title="SUKHA PMS API")

app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"status": "Sukha PMS Backend Running"}
