import json

with open(r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\flight_network.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

with open(r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\india_path.txt", "r", encoding="utf-8") as f:
    india_path_d = f.read().strip()

dataset_json = json.dumps(dataset)

print(f"Loaded dataset: {len(dataset['flights'])} flights, India path length: {len(india_path_d)}")
