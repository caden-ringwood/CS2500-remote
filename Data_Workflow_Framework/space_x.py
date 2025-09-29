import requests
import json
import pandas as pd

# 1. Get the raw Starlink JSON data
url = "https://api.spacexdata.com/v4/starlink"
response = requests.get(url)
data = response.json()

print(f"Downloaded {len(data)} Starlink satellite records")

# 2. Save raw JSON to a file
with open("starlink_raw.json", "w") as f:
    json.dump(data, f, indent=4)

print("Saved raw JSON to starlink_raw.json")

# 3. Flatten JSON into a pandas DataFrame
df = pd.json_normalize(data)

# 4. Keep only useful columns
important_cols = [
    "spaceTrack.OBJECT_NAME",
    "spaceTrack.LAUNCH_DATE",
    "spaceTrack.DECAYED",
    "spaceTrack.PERIOD",
    "height_km",
    "latitude",
    "longitude",
    "velocity_kms",
    "id"
]

# Keep only the columns that exist in the data
cols_to_keep = [col for col in important_cols if col in df.columns]
df = df[cols_to_keep]

# Rename columns for clarity
rename_map = {
    "spaceTrack.OBJECT_NAME": "name",
    "spaceTrack.LAUNCH_DATE": "launch_date",
    "spaceTrack.DECAYED": "decayed",
    "spaceTrack.PERIOD": "period",
    "height_km": "height_km",
    "latitude": "latitude",
    "longitude": "longitude",
    "velocity_kms": "velocity_kms",
    "id": "id"
}
df = df.rename(columns=rename_map)
df['decayed'] = df['decayed'].astype(bool)


# 5. Save refined data to CSV
df.to_csv("starlink.csv", index=False)

df_decayed = df[df['decayed']]
print(f"Number of decayed satellites: {len(df_decayed)}")
df_active = df[~df['decayed']]
print(f"Number of active satellites: {len(df_active)}")

print(df.head())
