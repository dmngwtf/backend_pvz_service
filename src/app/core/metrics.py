from prometheus_client import Counter, Histogram, make_asgi_app
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.custom_logging import setup_logging

logger = setup_logging()

# Технические метрики
REQUEST_COUNT = Counter("pvz_requests_total", "Total number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("pvz_request_latency_seconds", "Request latency", ["method", "endpoint"])

# Бизнесовые метрики
PVZ_CREATED = Counter("pvz_created_total", "Total number of PVZ created")
RECEPTIONS_CREATED = Counter("pvz_receptions_created_total", "Total number of receptions created")
PRODUCTS_ADDED = Counter("pvz_products_added_total", "Total number of products added")

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        method = request.method
        REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

        with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
            response = await call_next(request)

        return response