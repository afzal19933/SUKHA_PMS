from fastapi import FastAPI

app = FastAPI(title="SUKHA PMS API")

@app.get("/")
def root():
    return {"status": "Sukha PMS Backend Running"}
