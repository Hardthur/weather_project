from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Active CORS sur toutes les routes

# Clé API OpenWeather
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
AIR_POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
UV_INDEX_URL = "https://api.openweathermap.org/data/2.5/uvi"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Weather API! Use /weather?city=Paris, /air_quality?city=Paris or /uv_index?city=Paris"}), 200

@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Veuillez fournir un nom de ville."}), 400

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "main" not in data:
        return jsonify({"error": "Ville non trouvée."}), 404

    return jsonify({
        "city": city,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    })

@app.route("/air_quality", methods=["GET"])
def air_quality():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Veuillez fournir un nom de ville."}), 400

    # Récupération des coordonnées de la ville
    params = {"q": city, "appid": API_KEY}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "coord" not in data:
        return jsonify({"error": "Ville non trouvée."}), 404

    lat, lon = data["coord"]["lat"], data["coord"]["lon"]

    # Récupération de la pollution de l'air
    air_params = {"lat": lat, "lon": lon, "appid": API_KEY}
    air_response = requests.get(AIR_POLLUTION_URL, params=air_params)
    air_data = air_response.json()

    if "list" not in air_data:
        return jsonify({"error": "Données de pollution indisponibles."}), 404

    air_quality_index = air_data["list"][0]["main"]["aqi"]

    return jsonify({
        "city": city,
        "air_quality_index": air_quality_index
    })

@app.route("/uv_index", methods=["GET"])
def uv_index():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "Veuillez fournir un nom de ville."}), 400

    # Récupération des coordonnées de la ville
    params = {"q": city, "appid": API_KEY}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "coord" not in data:
        return jsonify({"error": "Ville non trouvée."}), 404

    lat, lon = data["coord"]["lat"], data["coord"]["lon"]

    # Récupération de l’indice UV
    uv_params = {"lat": lat, "lon": lon, "appid": API_KEY}
    uv_response = requests.get(UV_INDEX_URL, params=uv_params)
    uv_data = uv_response.json()

    if "value" not in uv_data:
        return jsonify({"error": "Données UV indisponibles."}), 404

    uv_value = uv_data["value"]

    return jsonify({
        "city": city,
        "uv_index": uv_value
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
