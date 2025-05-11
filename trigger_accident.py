import sys
import traci
import utm

# Ensure UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

# SUMO configuration file
SUMO_CONFIG = "osm.sumocfg"
ACCIDENT_DURATION = 60  # Duration in seconds
ACCIDENT_IMPACT_RADIUS = 20  # Affected radius around the accident

# SUMO netOffset from osm.net.xml
x_offset, y_offset = -712702.83, -3164251.44

# Validate command-line arguments
if len(sys.argv) < 3:
    print("Usage: python trigger_accident.py <lat> <lon>")
    sys.exit(1)

# Convert latitude/longitude to SUMO coordinates
accident_lat = float(sys.argv[1])
accident_lon = float(sys.argv[2])
utm_x, utm_y, _, _ = utm.from_latlon(accident_lat, accident_lon)

# Adjust for SUMO netOffset
accident_x = utm_x - x_offset
accident_y = utm_y - y_offset

print(f"Triggering accident at SUMO coordinates: ({accident_x}, {accident_y})")

# Start SUMO with TraCI
traci.start(["sumo", "-c", SUMO_CONFIG])

try:
    for _ in range(ACCIDENT_DURATION):
        vehicles = traci.vehicle.getIDList()

        for vehicle in vehicles:
            try:
                x, y = traci.vehicle.getPosition(vehicle)
                distance = ((x - accident_x) ** 2 + (y - accident_y) ** 2) ** 0.5

                if distance <= ACCIDENT_IMPACT_RADIUS:
                    road_id = traci.vehicle.getRoadID(vehicle)
                    route = traci.vehicle.getRoute(vehicle)

                    if road_id in route:  # Ensure vehicle is on the correct road segment
                        traci.vehicle.slowDown(vehicle, 0, ACCIDENT_DURATION)  # Gradual stop
                        print(f"{vehicle} affected at {road_id}")

            except traci.TraCIException:
                continue  # Skip invalid vehicle data
        
        traci.simulationStep()  # Advance SUMO simulation

    print(f"Accident successfully triggered at ({accident_lat}, {accident_lon}) for {ACCIDENT_DURATION} seconds.")

finally:
    traci.close()
