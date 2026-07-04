from pathlib import Path
import sys

# Aggiunge la root del progetto al path di Python.
# Serve per permettere a pytest, anche su AWS CodeBuild,
# di importare correttamente app.py dalla cartella principale.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

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