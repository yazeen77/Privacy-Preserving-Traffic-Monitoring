import traci
import pandas as pd
import time
import os
import utm

# SUMO Configuration
sumo_cmd = ["sumo", "-c", "osm.sumocfg", "--step-length=1"]
raw_data_file = "data/raw_traffic_data.csv"
columns = ["timestamp", "vehicle_id", "lat", "lon", "speed", "edge", "vehicle_count"]

# SUMO netOffset from osm.net.xml
x_offset, y_offset = -712702.83, -3164251.44

# Ensure data directory exists
os.makedirs(os.path.dirname(raw_data_file), exist_ok=True)

# Delete old raw traffic data
if os.path.exists(raw_data_file):
    os.remove(raw_data_file)
    print(f"🗑️ Old data removed: {raw_data_file}")

def convert_utm_to_latlon(x, y):
    utm_x, utm_y = x - x_offset, y - y_offset
    lat, lon = utm.to_latlon(utm_x, utm_y, 43, "N")
    return lat, lon

# Start SUMO
traci.start(sumo_cmd)
print("🚦 SUMO started for raw data generation...")
for _ in range(700):
    traci.simulationStep()

vehicle_positions = {}  
step = 700

vehicle_positions = {}
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    timestamp = time.time()
    
    vehicle_ids = set(traci.vehicle.getIDList())
    updated_positions = {}
    edge_vehicle_count = {}

    for vid in vehicle_ids:
        x, y = traci.vehicle.getPosition(vid)
        speed = traci.vehicle.getSpeed(vid)
        edge = traci.vehicle.getRoadID(vid)
        lat, lon = convert_utm_to_latlon(x, y)
        
        updated_positions[vid] = (lat, lon, speed, edge)
        edge_vehicle_count[edge] = edge_vehicle_count.get(edge, 0) + 1

    vehicle_positions.update(updated_positions)

    df_data = [[timestamp, vid, *vehicle_positions[vid], edge_vehicle_count.get(vehicle_positions[vid][3], 1)] for vid in vehicle_positions]
    
    if df_data:
        df = pd.DataFrame(df_data, columns=columns)
        df.to_csv(raw_data_file, mode='w', header=True, index=False)
        print(f"✅ Dataset updated: {raw_data_file}")

    time.sleep(0.5)

traci.close()
print("✅ SUMO simulation completed. Raw dataset ready.")
