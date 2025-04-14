from fastapi import FastAPI
from fastapi.routing import APIRoute
from prometheus_client import make_asgi_app
from app.api.routes import auth, pvz, receptions, products
from app.core.custom_logging import setup_logging
from app.core.metrics import MetricsMiddleware
import threading
from app.grpc.server import serve as grpc_serve

app = FastAPI(title="PVZ Service", version="1.0.0")
logger = setup_logging()


app.add_middleware(MetricsMiddleware)


app.include_router(auth.router)
app.include_router(pvz.router)
app.include_router(receptions.router)
app.include_router(products.router)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to PVZ Service"}

threading.Thread(target=grpc_serve, daemon=True).start()