import traci
import pickle
import os
import xml.etree.ElementTree as ET
import utm

# SUMO configuration file
sumo_cfg = r"C:\Yazeen\Coding\Projects\Traffic Monitoring System - Copy\osm.sumocfg"

# Read netOffset from osm.net.xml
NET_XML_FILE = "osm.net.xml"
tree = ET.parse(NET_XML_FILE)
root = tree.getroot()
net_offset = root.find("location")
if net_offset is not None:
    x_offset, y_offset = map(float, net_offset.get("netOffset").split(","))
else:
    raise ValueError("netOffset missing from osm.net.xml!")

# Extract all road segments dynamically
segment_to_sumo_coords = {}
for edge in root.findall("edge"):
    edge_id = edge.get("id")
    if edge_id.startswith(":"):  # Skip internal edges
        continue
    
    lanes = edge.findall("lane")
    if lanes:
        first_lane = lanes[0]
        shape = first_lane.get("shape")
        
        if shape:
            points = shape.split()
            utm_x, utm_y = map(float, points[0].split(","))  # First point of the lane
            segment_to_sumo_coords[edge_id] = (utm_x, utm_y)

# Convert SUMO coordinates to Lat/Lon
def convert_to_latlon(segment, sumo_x, sumo_y):
    # Subtract netOffset instead of adding
    utm_x = sumo_x - x_offset
    utm_y = sumo_y - y_offset

    # Debugging print
    print(f"Debug: Segment {segment} | SUMO ({sumo_x}, {sumo_y}) → Adjusted UTM ({utm_x}, {utm_y})")

    # Ensure UTM coordinates are within a valid range
    if not (100000 <= utm_x <= 999999 and 0 <= utm_y <= 10000000):
        raise ValueError(f"Invalid UTM coordinates for {segment}: ({utm_x}, {utm_y})")

    lat, lon = utm.to_latlon(utm_x, utm_y, 43, "N")
    return lat, lon

# Process all road segments
segment_to_latlon = {seg: convert_to_latlon(seg, x, y) for seg, (x, y) in segment_to_sumo_coords.items()}

# Save updated segment-to-LatLon mapping
encoder_path = "ml_model/road_segment_encoder.pkl"
os.makedirs(os.path.dirname(encoder_path), exist_ok=True)
with open(encoder_path, "wb") as f:
    pickle.dump(segment_to_latlon, f)

print(f"Updated road_segment_encoder.pkl with lat/lon for {len(segment_to_latlon)} segments!")
