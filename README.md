
# Privacy-Preserving Traffic Monitoring Using Machine Learning Analytics

## Overview

This project is a **Flask-based web application** integrated with **SUMO (Simulation of Urban Mobility)** to simulate, process, and visualize real-time traffic data in **Rajpath, Delhi**, while ensuring privacy using **geo-indistinguishability** techniques. The system visualizes traffic data on **OpenStreetMap**, predicts congestion using **machine learning**, and differentiates views for public users and traffic authorities.

---

## Features

- 🔁 **Live SUMO Traffic Simulation**: Vehicle data is generated dynamically using SUMO and TraCI.
- 🔒 **Privacy-Preserving Mechanism**: Applies geo-indistinguishability to anonymize coordinates in the processed dataset.
- 🤖 **ML-Based Congestion Prediction**: Predicts congestion severity from traffic stats using trained ML models.
- 🗺️ **Interactive Map (User View)**: Displays predicted congestion levels via route coloring.
- 👮 **Authority View with Login**: Access to raw traffic data during abnormal congestion events.
- ⚠️ **Manual Accident Trigger**: Button to simulate an accident and test system response.
- 🌐 **Dual View Architecture**:
  - **Public View**: Shows anonymized, ML-predicted congestion levels.
  - **Authority View**: Shows raw, non-anonymized data with detailed info.

---

## Project Structure

```
Traffic-Monitoring-System/
│── app.py                        # Main Flask application
│── ml_model.py                   # ML model for congestion prediction
│── process_traffic_data.py       # Congestion analysis and ML input prep
│── apply_anonymization.py        # Geo-indistinguishability for location data
│── sumo_simulation.py            # SUMO TraCI integration and live data feed
│── routes/
│   ├── authority.py              # Routes for login and authority dashboard
│   ├── public.py                 # Routes for public map and data
│── templates/
│   ├── index.html                # Public map UI (OpenStreetMap + Leaflet)
│   ├── authority.html            # Authority dashboard view
│   ├── login.html                # Login interface
│── static/
│   ├── styles.css                # Frontend styles
│── data/
│   ├── raw_traffic_data.csv      # Dynamically updated raw data
│   ├── processed_data.csv        # Anonymized and ML-enhanced data
│── simulation/
│   ├── rajpath.net.xml           # Rajpath road network
│   ├── rajpath.rou.xml           # Route configuration with reduced congestion
│── requirements.txt              # Python dependencies
│── README.md                     # Project documentation
```

---

## Installation

### Prerequisites

- Python 3.8+
- SUMO (Simulation of Urban Mobility)
- pip
- Virtual environment (recommended)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/Traffic-Monitoring-System.git
   cd Traffic-Monitoring-System
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app (this will also launch the SUMO-GUI simulation):

   ```bash
   python app.py
   ```

5. Open your browser and visit **http://127.0.0.1:5000/**

---

## Usage

- 🗺 **Public View**:
  - View predicted congestion in Rajpath using color-coded routes (green to red).
  - Congestion levels update in real-time as SUMO simulation runs.

- 🔐 **Authority View**:
  - Login to access real-time raw vehicle data (latitude, longitude, speed).
  - View congestion tables, vehicle markers, and accident simulation effects.

- 🚨 **Accident Trigger**:
  - Use the "Trigger Accident" button to simulate a congestion-causing event dynamically.

---

## Technologies Used

- **Simulation**: SUMO, TraCI
- **Backend**: Flask, Pandas
- **Frontend**: HTML, CSS, JavaScript, Leaflet.js
- **Machine Learning**: Scikit-learn
- **Anonymization**: Geo-indistinguishability (Laplace noise)
- **Visualization**: OpenStreetMap, Leaflet.heat

---

## Future Enhancements

- ✅ Integrate real traffic APIs (Google Maps, HERE).
- ✅ Advanced anonymization (k-anonymity, differential privacy).
- 🚀 Cloud deployment (Heroku, AWS EC2).
- 🔐 Blockchain for secure traffic reporting.

---

## License

This project is licensed under the **MIT License**.

---

**Author**: Muhammed Yazeen S
