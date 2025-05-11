import xml.etree.ElementTree as ET
import csv
import os
import utm

# Load netOffset from SUMO network file
NET_XML_FILE = "osm.net.xml"
OUTPUT_CSV_FILE = "data/edges.csv"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Read netOffset from `osm.net.xml`
tree = ET.parse(NET_XML_FILE)
root = tree.getroot()
net_offset = root.find("location")
if net_offset is not None:
    x_offset, y_offset = map(float, net_offset.get("netOffset").split(","))
else:
    raise ValueError("netOffset missing from osm.net.xml!")

edges_data = []

# Iterate over each <edge> in the XML
for edge in root.findall("edge"):
    edge_id = edge.get("id")
    
    # Skip internal edges (start with ':')
    if edge_id.startswith(":"):
        continue

    lanes = edge.findall("lane")
    if len(lanes) > 0:
        first_lane = lanes[0]  # Use first lane for coordinates
        shape = first_lane.get("shape")
        
        if shape:
            points = shape.split()
            utm_x_start, utm_y_start = map(float, points[0].split(","))
            utm_x_end, utm_y_end = map(float, points[-1].split(","))

            # Correct netOffset application (subtract instead of adding)
            adj_x_start, adj_y_start = utm_x_start - x_offset, utm_y_start - y_offset
            adj_x_end, adj_y_end = utm_x_end - x_offset, utm_y_end - y_offset

            # Convert UTM to lat/lon (using Zone 43N for Rajpath)
            lat_start, lon_start = utm.to_latlon(adj_x_start, adj_y_start, 43, "N")
            lat_end, lon_end = utm.to_latlon(adj_x_end, adj_y_end, 43, "N")

            edges_data.append([edge_id, lat_start, lon_start, lat_end, lon_end])

# Write extracted data to CSV
with open(OUTPUT_CSV_FILE, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["edge_id", "lat_start", "lon_start", "lat_end", "lon_end"])
    writer.writerows(edges_data)

print(f"Extracted {len(edges_data)} edges and saved to '{OUTPUT_CSV_FILE}'.")
