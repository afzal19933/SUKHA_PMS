from fastapi import FastAPI

app = FastAPI(title="Sukha PMS API")

@app.get("/")
def read_root():
    return {"message": "Sukha PMS Backend Running"}
