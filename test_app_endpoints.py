from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

print("1. Testing GET / ...")
resp = client.get("/")
assert resp.status_code == 200
assert "DOMINO SKY" in resp.text
print("   ✓ GET / success! HTML length:", len(resp.text))

print("\n2. Testing GET /api/network ...")
resp = client.get("/api/network")
assert resp.status_code == 200
data = resp.json()
assert len(data["airports"]) == 16
assert len(data["flights"]) == 70
assert len(data["connections"]) == 21
assert len(data["crews"]) == 16
assert len(data["spare_aircraft"]) == 2
print("   ✓ GET /api/network verified! 16 airports, 70 flights, 21 connections, 16 crews, 2 spares.")

print("\n3. Testing POST /api/simulate for BOM 15:00-16:30 ...")
resp = client.post("/api/simulate", json={
    "closed_airport": "BOM",
    "closure_start": "15:00",
    "closure_end": "16:30"
})
assert resp.status_code == 200
sim_data = resp.json()
kpis = sim_data["kpis"]
print(f"   ✓ Simulation result: {kpis['delayed_flights']} delayed flights, {kpis['total_delay_minutes']} delay mins, {kpis['crew_duty_violations']} crew violations")
assert kpis["delayed_flights"] == 3
assert kpis["total_delay_minutes"] == 150
assert kpis["crew_duty_violations"] == 1

print("\n4. Testing POST /api/evaluate_recovery ...")
resp = client.post("/api/evaluate_recovery", json={
    "closed_airport": "BOM",
    "closure_start": "15:00",
    "closure_end": "16:30"
})
assert resp.status_code == 200
rec_data = resp.json()
options = rec_data["options"]
print(f"   ✓ Generated {len(options)} recovery options. Top option: {options[0]['title']}")

print("\n5. Testing POST /api/ai_briefing ...")
resp = client.post("/api/ai_briefing", json={
    "simulation_data": sim_data,
    "recovery_options": options
})
assert resp.status_code == 200
ai_data = resp.json()
print("   ✓ AI briefing generated successfully!")
print("   AI Summary snippet:", ai_data["incident_summary"][:120], "...")

print("\nALL SERVER ENDPOINTS VERIFIED 100% OPERATIONAL!")
