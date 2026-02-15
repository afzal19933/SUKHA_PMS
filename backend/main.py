from fastapi import FastAPI
from app.routes.auth import router as auth_router

app = FastAPI(title="SUKHA PMS API")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "Sukha PMS Backend Running"}
