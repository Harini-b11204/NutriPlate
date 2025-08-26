from flask import Flask, request, jsonify, render_template_string
from main import detect_food, classify_food, estimate_freshness, get_nutrition

app = Flask(__name__)

@app.route('/')
def home():
    return "🍽️ NutriPlate is running on Vercel!"

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    return jsonify({"food": "Strawberry", "calories": 4})
