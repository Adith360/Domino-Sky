import json
import os

data_path = r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\flight_network.json"
with open(data_path, "r", encoding="utf-8") as f:
    network_data = json.load(f)

json_str = json.dumps(network_data)

# Let's read static/index.html
html_path = r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\static\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect how to add the embedded dataset and client-side engine
print("Successfully loaded flight_network.json and static/index.html")
print(f"Network data: {len(network_data['flights'])} flights, {len(network_data['airports'])} airports")
