import json
from simulator import SimulationEngine

engine = SimulationEngine()

# Test several scenarios in Python
scenarios = [
    ("BOM", "15:00", "16:30"),
    ("BOM", "07:30", "09:00"),
    ("DEL", "08:00", "10:00"),
    ("CCU", "12:00", "14:00"),
    ("BLR", "09:00", "11:00")
]

ground_truth = {}
for apt, s, e in scenarios:
    res = engine.run_simulation(apt, s, e)
    opts = engine.evaluate_recovery_options(apt, s, e)
    ground_truth[f"{apt}_{s}_{e}"] = {
        "kpis": res["kpis"],
        "options_count": len(opts),
        "top_option": opts[0]["title"] if opts else None,
        "top_delta": opts[0]["delta"] if opts else None
    }

print("Ground Truth Summary:")
for k, v in ground_truth.items():
    print(f"  {k}: Delayed={v['kpis']['delayed_flights']}, Mins={v['kpis']['total_delay_minutes']}, Stranded Pax={v['kpis']['stranded_passengers']}, Crew Viols={v['kpis']['crew_duty_violations']}")
    if v["top_option"]:
        print(f"      Top Rec: {v['top_option']} | Delay saved: -{v['top_delta']['delay_minutes_saved']}m, Pax saved: +{v['top_delta']['stranded_pax_saved']}")

with open(r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\ground_truth.json", "w") as f:
    json.dump(ground_truth, f, indent=2)
