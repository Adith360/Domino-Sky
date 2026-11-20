from simulator import SimulationEngine

engine = SimulationEngine()
print("Initialized SimulationEngine successfully.")

# Test BOM closure 07:30 to 09:00
res = engine.run_simulation("BOM", "07:30", "09:00")
print(f"BOM 07:30-09:00:")
print(f"  KPIs: Delayed={res['kpis']['delayed_flights']}, Minutes={res['kpis']['total_delay_minutes']}, Stranded Pax={res['kpis']['stranded_passengers']}, Crew Violations={res['kpis']['crew_duty_violations']}")

# Test Recovery Options
print("\nEvaluating Recovery Options for BOM 07:30-09:00...")
options = engine.evaluate_recovery_options("BOM", "07:30", "09:00")
print(f"Generated {len(options)} recovery options:")
for i, opt in enumerate(options):
    print(f"  [{i+1}] {opt['title']} ({opt['type']})")
    print(f"      Delta: -{opt['delta']['delay_minutes_saved']} delay mins, +{opt['delta']['stranded_pax_saved']} pax saved, INR {opt['delta']['cost_saved_inr']:,} saved")

# Test CCU closure
print("\nEvaluating CCU 12:00-14:00...")
res_ccu = engine.run_simulation("CCU", "12:00", "14:00")
print(f"  KPIs: Delayed={res_ccu['kpis']['delayed_flights']}, Minutes={res_ccu['kpis']['total_delay_minutes']}, Stranded Pax={res_ccu['kpis']['stranded_passengers']}, Crew Violations={res_ccu['kpis']['crew_duty_violations']}")
