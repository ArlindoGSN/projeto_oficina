from fastapi import status
from fastapi.testclient import TestClient

from src.app import app
from src.database import init_db

client = TestClient(app)


def test_register_user_success_and_duplicate():
    # garante que o DB está inicializado limpo
    init_db()

    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "secret123",
    }

    # Primeiro registro deve retornar 201
    response = client.post("/register", json=payload)
    print(response.status_code, response.json())
    assert response.status_code == status.HTTP_201_CREATED

    # Segundo registro com mesmo username/email deve retornar 400
    response2 = client.post("/register", json=payload)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response2.json().get("detail", "")
