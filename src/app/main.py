from fastapi import FastAPI

app = FastAPI(title="PVZ Service", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to PVZ Service"}