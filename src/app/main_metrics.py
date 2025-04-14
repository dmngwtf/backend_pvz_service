from prometheus_client import start_http_server
from app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY, PVZ_CREATED, RECEPTIONS_CREATED, PRODUCTS_ADDED
from app.core.custom_logging import setup_logging

logger = setup_logging()

if __name__ == "__main__":
    logger.info("Starting Prometheus metrics server on port 9000")
    start_http_server(9000)
    logger.info("Metrics server running. Access at http://localhost:9000/metrics")
    import time
    while True:
        time.sleep(1000)