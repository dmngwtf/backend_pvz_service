import grpc
from concurrent import futures
from app.db.database import get_db
import pvz_pb2
import pvz_pb2_grpc
from app.core.custom_logging import setup_logging

logger = setup_logging()

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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pvz_pb2_grpc.add_PVZServiceServicer_to_server(PVZService(), server)
    server.add_insecure_port("[::]:3000")
    logger.info("gRPC server started on port 3000")
    server.start()
    server.wait_for_termination()