import grpc
from concurrent import futures
from app.db.database import get_db
from app.grpc import pvz_pb2
from app.grpc import pvz_pb2_grpc
from app.core.custom_logging import setup_logging

try:
    from app.db.database import get_db
except ImportError as e:
    print(f"Failed to import get_db: {e}")
    raise
try:
    import pvz_pb2
    import pvz_pb2_grpc
except ImportError as e:
    print(f"Failed to import pvz_pb2/pvz_pb2_grpc: {e}")
    raise
try:
    from app.core.custom_logging import setup_logging
except ImportError as e:
    print(f"Failed to import setup_logging: {e}")
    raise

print("Starting gRPC server initialization")
logger = setup_logging()
print("Logger initialized")

class PVZService(pvz_pb2_grpc.PVZServiceServicer):
    def GetPVZList(self, request, context):
        logger.info("gRPC GetPVZList called")
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, registration_date, city FROM pvzs")
            pvzs = cursor.fetchall()

            response = pvz_pb2.GetPVZListResponse()
            for pvz in pvzs:
                response.pvzs.add(
                    id=str(pvz["id"]),
                    registration_date=pvz["registration_date"].isoformat(),
                    city=pvz["city"]
                )
            return response

def serve():
    print("Creating gRPC server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pvz_pb2_grpc.add_PVZServiceServicer_to_server(PVZService(), server)
    server.add_insecure_port("[::]:3000")
    logger.info("gRPC server started on port 3000")
    print("gRPC server listening on port 3000")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    print("Running gRPC server")
    serve()