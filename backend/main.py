from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.unit import router as unit_router
from app.core.database import create_db_and_tables
# Import models so tables get created
from app.models.user import User
from app.models.unit import Unit   # 👈 ADD THIS LINE
from app.routes.unit import router as unit_router
from app.models.stay import Stay
from app.routes.stay import router as stay_router





app = FastAPI(title="SUKHA PMS API")

app.include_router(auth_router)
app.include_router(unit_router)
app.include_router(stay_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"status": "Sukha PMS Backend Running"}
