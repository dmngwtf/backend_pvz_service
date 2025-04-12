from fastapi import FastAPI
from app.api.routes import auth, pvz, receptions, products

app = FastAPI(title="PVZ Service", version="1.0.0")

app.include_router(auth.router)
app.include_router(pvz.router)
app.include_router(receptions.router)
app.include_router(products.router)

@app.get("/")
async def root():
    return {"message": "Welcome to PVZ Service"}