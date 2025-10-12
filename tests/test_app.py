from fastapi import status
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Olá Mundo"}
