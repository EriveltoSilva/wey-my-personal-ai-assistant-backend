from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root_deve_retornar_ola_mundo():
    """Test the root endpoint.
    A: Arrange
    A: Act
    A: Assert
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
