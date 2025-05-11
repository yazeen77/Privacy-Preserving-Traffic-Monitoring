import pandas as pd
import numpy as np
import os

# Load processed traffic data
data_file = "data/processed_traffic_data.csv"

# Check if file exists before proceeding
if not os.path.exists(data_file) or os.stat(data_file).st_size == 0:
    print(f" Error: {data_file} is missing or empty.")
    exit(1)

df = pd.read_csv(data_file)

# Define Laplace noise function for geo-indistinguishability
def add_laplace_noise(value, sensitivity=0.0001, epsilon=0.1, min_val=None, max_val=None):
    if pd.isna(value):  
        return value
    noise = np.random.laplace(0, sensitivity / epsilon)
    return np.clip(value + noise, min_val, max_val) if min_val and max_val else value + noise

# Drop NaN locations before applying noise
df.dropna(subset=["lat", "lon"], inplace=True)

# Use Rajpath-specific bounding box to prevent invalid locations
lat_min, lat_max = 28.58, 28.64  
lon_min, lon_max = 77.17, 77.27  

df["lat"] = df["lat"].apply(lambda x: add_laplace_noise(x, min_val=lat_min, max_val=lat_max))
df["lon"] = df["lon"].apply(lambda x: add_laplace_noise(x, min_val=lon_min, max_val=lon_max))

# Save anonymized data back
df.to_csv(data_file, index=False)

print(" Processed traffic data updated with anonymized coordinates.")
