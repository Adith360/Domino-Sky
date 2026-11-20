import json

# Load dataset
with open(r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\flight_network.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

dataset_json = json.dumps(dataset)

with open(r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\static\index.html", "r", encoding="utf-8") as f:
    existing_html = f.read()

# Let's inspect where EMBEDDED_DATA can be placed
# In static/index.html, let's see how it's structured
print("Read existing index.html, length:", len(existing_html))
