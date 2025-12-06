from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# IMPORTANT: Ensure your .env file has OPENWEATHER_API_KEY=YOUR_KEY_HERE
API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/')
def index():
    """
    Renders the main HTML page.
    Assumes 'index.html' is located in a 'templates' directory.
    """
    return render_template("index.html")

# --- MODIFIED ROUTE TO HANDLE CITY OR LAT/LON ---
@app.route('/get-weather')
def get_weather():
    """
    Fetches the 5-day weather forecast data from OpenWeatherMap.
    Accepts either a 'city' name or 'lat' and 'lon' coordinates.
    """
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    
    if API_KEY is None:
        # 500 Internal Server Error if the key is missing on the server
        return jsonify({'cod': '500', 'message': 'API Key not configured on the server.'}), 500

    if city:
        # Use city name if provided (for manual search)
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
    elif lat and lon:
        # Use latitude and longitude if provided (for geolocation)
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric'
        }
    else:
        # 400 Bad Request if no parameters are provided
        return jsonify({'cod': '400', 'message': 'City or geographical coordinates (lat/lon) are required.'}), 400

    try:
        # Make the request to the OpenWeatherMap API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad HTTP codes (4xx or 5xx)
        return jsonify(response.json())
    
    except requests.exceptions.RequestException as e:
        app.logger.error(f"OpenWeatherMap API request failed: {e}")
        # Return a user-friendly error message
        return jsonify({'cod': response.status_code, 'message': f"External API Error: {response.text}"}), response.status_code

if __name__ == '__main__':
    # Running the app with debug=True for development.
    # host='0.0.0.0' allows access from outside the container/localhost if needed.
    app.run(debug=True, host='0.0.0.0')
