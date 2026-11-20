from simulator import SimulationEngine

engine = SimulationEngine()
print("Evaluating Recovery Options for CCU 12:00-14:00...")
options = engine.evaluate_recovery_options("CCU", "12:00", "14:00")
print(f"Generated {len(options)} recovery options for CCU:")
for i, opt in enumerate(options):
    print(f"  [{i+1}] {opt['title']} ({opt['type']})")
    print(f"      Delta: -{opt['delta']['delay_minutes_saved']} delay mins, +{opt['delta']['stranded_pax_saved']} pax saved, {opt['delta']['crew_violations_saved']} crew saved, INR {opt['delta']['cost_saved_inr']:,} saved")
