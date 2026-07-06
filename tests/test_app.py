from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import app


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["version"] == "1.2.0"


def test_home_endpoint():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Weather Edge Monitor" in response.data
    assert b"name=\"city\"" in response.data



def test_weather_endpoint_missing_city():
    client = app.test_client()

    response = client.get("/api/weather")

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data


def test_weather_endpoint_success(monkeypatch):
    """
    Test dell'endpoint /api/weather senza chiamare davvero Open-Meteo.

    Usiamo monkeypatch per simulare la risposta delle funzioni esterne.
    In questo modo i test restano veloci e non dipendono dalla rete.
    """

    def fake_get_coordinates(city_name):
        return {
            "name": "Modena",
            "country": "Italy",
            "admin1": "Emilia-Romagna",
            "latitude": 44.6471,
            "longitude": 10.9252,
            "timezone": "Europe/Rome"
        }

    def fake_get_current_weather(latitude, longitude):
        return {
            "current": {
                "temperature_2m": 22.5,
                "relative_humidity_2m": 60,
                "wind_speed_10m": 7.2,
                "time": "2026-07-05T10:00"
            }
        }

    monkeypatch.setattr("app.get_coordinates", fake_get_coordinates)
    monkeypatch.setattr("app.get_current_weather", fake_get_current_weather)

    client = app.test_client()

    response = client.get("/api/weather?city=Modena")

    assert response.status_code == 200

    data = response.get_json()

    assert data["city"] == "Modena"
    assert data["country"] == "Italy"
    assert data["temperature"] == 22.5
    assert data["humidity"] == 60
    assert data["wind_speed"] == 7.2


def test_home_endpoint_with_weather(monkeypatch):
    def fake_get_weather_by_city(city):
        return {
            "city": "Modena",
            "region": "Emilia-Romagna",
            "country": "Italy",
            "latitude": 44.6471,
            "longitude": 10.9252,
            "temperature": 22.5,
            "humidity": 60,
            "wind_speed": 7.2,
            "time": "2026-07-05T10:00"
        }, None, 200

    monkeypatch.setattr("app.get_weather_by_city", fake_get_weather_by_city)

    client = app.test_client()

    response = client.get("/?city=Modena")

    assert response.status_code == 200
    assert b"Modena" in response.data
    assert b"22.5" in response.data
    assert b"60" in response.data