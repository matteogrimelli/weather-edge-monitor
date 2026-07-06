from flask import Flask, jsonify, request, render_template
import requests


app = Flask(__name__)

APP_VERSION = "1.2.0"

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


@app.route("/")
def home():
    """
    HTML dashboard.

    If the user provides a city parameter, the page shows current weather data.
    Example:
    /?city=Modena
    """
    city = request.args.get("city")
    weather = None
    error = None

    if city:
        try:
            weather, error, _ = get_weather_by_city(city)
        except requests.RequestException:
            error = "Unable to retrieve weather data"

    return render_template(
        "index.html",
        city=city,
        weather=weather,
        error=error,
        version=APP_VERSION
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "version": APP_VERSION
    })


def get_coordinates(city_name):
    """
    Converts a city name into geographic coordinates using Open-Meteo Geocoding API.
    """
    params = {
        "name": city_name,
        "count": 1,
        "language": "it",
        "format": "json"
    }

    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    if not results:
        return None

    location = results[0]

    return {
        "name": location.get("name"),
        "country": location.get("country"),
        "admin1": location.get("admin1"),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "timezone": location.get("timezone")
    }


def get_current_weather(latitude, longitude):
    """
    Retrieves current weather data for the given coordinates using Open-Meteo Forecast API.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


@app.route("/api/weather")
def api_weather():
    """
    REST endpoint that returns current weather data for a city.

    Example:
    /api/weather?city=Modena
    """
    city = request.args.get("city")

    if not city:
        return jsonify({
            "error": "Missing city parameter. Example: /api/weather?city=Modena"
        }), 400

    try:
        weather, error, status_code = get_weather_by_city(city)

        if error:
            return jsonify({
                "error": error
            }), status_code

        return jsonify(weather), 200

    except requests.RequestException:
        return jsonify({
            "error": "Unable to retrieve weather data"
        }), 500


def get_weather_by_city(city):
    """
    Retrieves normalized weather data for a city.

    This function is used both by the HTML dashboard and by the REST API.
    """
    location = get_coordinates(city)

    if location is None:
        return None, f"City not found: {city}", 404

    weather = get_current_weather(
        location["latitude"],
        location["longitude"]
    )

    current = weather.get("current", {})

    result = {
        "city": location["name"],
        "region": location["admin1"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "time": current.get("time")
    }

    return result, None, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)