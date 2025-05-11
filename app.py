from flask import Flask, jsonify, send_from_directory, request, session
import pandas as pd
import os
import subprocess
import json
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "supersecretkey"
CORS(app)

raw_data_file = "data/raw_traffic_data.csv"
processed_data_file = "data/processed_traffic_data.csv"
processed_vehicle_data_file = "data/processed_vehicle_data.csv"
config_file = "data/config.json"

# Start traffic extraction process
extract_process = subprocess.Popen(["python", "extract_traffic.py"])

# Create default config if missing
if not os.path.exists(config_file):
    with open(config_file, "w") as f:
        json.dump({"traffic_density": 50}, f)

# Process raw traffic data

def process_traffic_data():
    if os.path.exists(raw_data_file):
        subprocess.run(["python", "process_traffic_data.py"], check=True)

# Read processed traffic data

def read_traffic_data():
    if os.path.exists(processed_data_file):
        df = pd.read_csv(processed_data_file)
        if 'speed' not in df.columns:
            df['speed'] = 0  # Default if missing
        return df.to_dict(orient="records")
    return []

# Read raw traffic data for authority access

def read_authority_data():
    if os.path.exists(raw_data_file):
        df = pd.read_csv(raw_data_file)
        if 'speed' not in df.columns:
            df['speed'] = 0
        return df.to_dict(orient="records")
    return []

# Serve frontend

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

# API for public traffic data

@app.route("/traffic")
def get_traffic_data():
    process_traffic_data()
    return jsonify(read_traffic_data())

# API for authority access

@app.route("/authority")
def get_authority_data():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized access. Please log in."}), 403
    return jsonify(read_authority_data())

# API to trigger an accident

@app.route("/trigger_accident", methods=["POST"])
def trigger_accident():
    try:
        data = request.get_json()
        location = data if "lat" in data and "lon" in data else data.get("location", {})
        if not location:
            return jsonify({"error": "Valid location (lat, lon) required"}), 400

        result = subprocess.run(
            ["python", "trigger_accident.py", str(location["lat"]), str(location["lon"])],
            capture_output=True, text=True, check=True
        )
        return jsonify({"message": "Accident triggered successfully", "output": result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to trigger accident", "details": e.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API for authority login

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == "admin" and password == "password":
        session["logged_in"] = True
        session.permanent = True
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# API for logout

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("logged_in", None)
    return jsonify({"message": "Logged out successfully"}), 200

# API to check login status

@app.route("/check_login")
def check_login():
    return jsonify({"logged_in": session.get("logged_in", False)})

# Run Flask app

if __name__ == "__main__":
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        extract_process.terminate()