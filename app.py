from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get-weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
