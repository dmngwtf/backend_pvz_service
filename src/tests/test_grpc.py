import grpc
from app.grpc import pvz_pb2
from app.grpc import pvz_pb2_grpc
from app.main import app
from app.db.database import get_db
from app.core.security import create_token
from fastapi.testclient import TestClient
client = TestClient(app)

def setup_database():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products; DELETE FROM receptions; DELETE FROM pvzs;")

def test_grpc_get_pvz_list():
    setup_database()
    token = create_token({"role": "moderator"})
    client.post(
        "/pvz",
        json={"city": "Москва"},
        headers={"Authorization": f"Bearer {token}"}
    )

    with grpc.insecure_channel("localhost:3000") as channel:
        stub = pvz_pb2_grpc.PVZServiceStub(channel)
        response = stub.GetPVZList(pvz_pb2.GetPVZListRequest())
        assert len(response.pvzs) == 1
        assert response.pvzs[0].city == "Москва"