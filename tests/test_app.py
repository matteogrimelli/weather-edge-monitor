# Importa l'istanza Flask definita in app.py.
# Il blocco if __name__ == "__main__" non viene eseguito durante l'import,
# quindi il server non parte automaticamente durante i test.
from app import app


def test_health_endpoint():
    """
    Verifica che l'endpoint /health risponda correttamente.
    Questo endpoint sarà usato anche dalla pipeline locale e da AWS
    per controllare che l'applicazione sia attiva.
    """
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"


def test_home_endpoint():
    """
    Verifica che la homepage sia raggiungibile
    e contenga il nome dell'applicazione.
    """
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Weather Edge Monitor" in response.data